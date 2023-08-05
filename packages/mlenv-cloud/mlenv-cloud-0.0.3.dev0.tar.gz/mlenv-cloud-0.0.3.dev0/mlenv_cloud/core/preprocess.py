"""Module that makes the `entry_point` distribution ready."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import logging
import os
import sys
import tempfile


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    from nbconvert import PythonExporter  # pylint: disable=g-import-not-at-top
except ImportError:
    PythonExporter = None

try:
    # Available in a colab environment.
    from google.colab import _message  # pylint: disable=g-import-not-at-top
except ImportError:
    _message = None


def get_preprocessed_entry_point(
    entry_point,
    called_from_notebook=False,
    return_file_descriptor=False
):
    """Creates python script based on the given `entry_point`.
    This utility creates a new python script called `preprocessed_entry_point`
    based on the given `entry_point` input. This
    script will become the new Docker entry point python program.

    1. If `entry_point` is a python file name then `preprocessed_entry_point`
    will have the user given `entry_point`
    2. If `entry_point` is None and `run` is invoked inside of a python script,
    then `preprocessed_entry_point` will be this python script (sys.args[0]).
    3. If `entry_point` is an `ipynb` file, then `preprocessed_entry_point`
    will be the code from the notebook. This utility uses `nbconvert`
    to get the code from notebook.
    4. If `entry_point` is None and `run` is invoked inside of an `ipynb`
    notebook, then `preprocessed_entry_point` will be the code from the
    notebook. This utility uses `google.colab` client API to fetch the code.

    Args:
        entry_point: Optional string. File path to the python file or iPython
            notebook that contains the TensorFlow code.
            Note) This path must be in the current working directory tree.
            Example) 'train.py', 'training/mnist.py', 'mnist.ipynb'
            If `entry_point` is not provided, then
            - If you are in an iPython notebook environment, then the
                current notebook is taken as the `entry_point`.
            - Otherwise, the current python script is taken as the
                `entry_point`.
        called_from_notebook: Boolean. True if the API is run in a
            notebook environment.
        return_file_descriptor: Boolean. True if the file descriptor for the
            temporary file is also returned.
    Returns:
        The `preprocessed_entry_point` file path.
    Raises:
        RuntimeError: If invoked from Notebook but unable to access it.
            Typically, this is due to missing the `nbconvert` package.
    """

    # Set `MLENV_RUNNING_REMOTELY` env variable. This is required in order
    # to prevent running `mlenv.run` if we are already in a cloud environment.
    # This is applicable only when `entry_point` is None.
    script_lines = [
        "import os\n",
        'os.environ["MLENV_RUNNING_REMOTELY"]="1"\n',
    ]

    # If `entry_point` is not provided, detect if we are in a notebook
    # or a python script. Fetch the `entry_point`.
    if entry_point is None and not called_from_notebook:
        # Current python script is assumed to be the entry_point.
        entry_point = sys.argv[0]

    # Add user's code.
    if entry_point is not None and entry_point.endswith("py"):
        # We are using exec here to execute the user code object.
        # This will support use case where the user's program has a
        # main method.
        _, entry_point_file_name = os.path.split(entry_point)
        script_lines.append(
            'exec(open("{}").read())\n'.format(entry_point_file_name))
    else:
        if called_from_notebook:
            # Kaggle integration
            if os.getenv("KAGGLE_CONTAINER_NAME"):
                logger.info("Preprocessing Kaggle notebook...")
                py_content = _get_kaggle_notebook_content()
            else:
                # Colab integration
                py_content = _get_colab_notebook_content()
        else:
            if PythonExporter is None:
                raise RuntimeError(
                    "Unable to access iPython notebook. "
                    "Please make sure you have installed `nbconvert` package."
                )

            # Get the python code from the iPython notebook.
            (py_content, _) = PythonExporter().from_filename(entry_point)
            py_content = py_content.splitlines(keepends=True)

        # Remove any iPython special commands and add the python code
        # to script_lines.
        for line in py_content:
            if  line.strip().startswith("%"):
              raise RuntimeError("Magic commands '%' are not supported.")

            elif line.strip().startswith("!"):
              commands_list = line.strip()[1:].split(" ")
              script_lines.extend([
                  "import sys\n",
                  "import subprocess\n",
                  f"print(subprocess.run({commands_list}",
                  ",capture_output=True, text=True).stdout)\n"
              ])

            elif not (
                line.strip().startswith("get_ipython().system(")
            ):
                script_lines.append(line)

    # Create a tmp wrapped entry point script file.
    file_descriptor, output_file = tempfile.mkstemp(suffix=".py")
    with open(output_file, "w") as f:
        f.writelines(script_lines)

    # Returning file descriptor could be necessary for some os.close calls
    if return_file_descriptor:
      return (output_file, file_descriptor)
    else:
      return output_file


def _get_colab_notebook_content():
    """Returns the colab notebook python code contents."""
    response = _message.blocking_request("get_ipynb",
                                         request="",
                                         timeout_sec=200)
    if response is None:
        raise RuntimeError("Unable to get the notebook contents.")
    cells = response["ipynb"]["cells"]
    py_content = []
    for cell in cells:
        if cell["cell_type"] == "code":
            # Add newline char to the last line of a code cell.
            cell["source"][-1] += "\n"

            # Combine all code cells.
            py_content.extend(cell["source"])
    return py_content


def _get_kaggle_notebook_content():
    """Returns the kaggle notebook python code contents."""
    if PythonExporter is None:
        raise RuntimeError(
            # This should never occur.
            # `nbconvert` is always installed on Kaggle.
            "Please make sure you have installed `nbconvert` package."
        )
    from kaggle_session import UserSessionClient  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error
    kaggle_session_client = UserSessionClient()
    try:
        response = kaggle_session_client.get_exportable_ipynb()
        ipynb_stream = io.StringIO(response["source"])
        py_content, _ = PythonExporter().from_file(ipynb_stream)
        return py_content.splitlines(keepends=True)
    except:
        raise RuntimeError("Unable to get the notebook contents.")