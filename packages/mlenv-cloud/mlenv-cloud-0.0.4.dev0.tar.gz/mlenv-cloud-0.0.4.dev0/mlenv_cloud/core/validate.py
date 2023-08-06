"""Module that performs validations on the inputs to the `run` API."""

import os

from . import gcp


def validate(
    entry_point,
    requirements_txt,
    entry_point_args,
    docker_image_build_bucket,
    called_from_notebook,
    docker_parent_image=None,
):
    """Validates the inputs.
    Args:
        entry_point: Optional string. File path to the python file or iPython
            notebook that contains the TensorFlow code.
        requirements_txt: Optional string. File path to requirements.txt file
            containing aditionally pip dependencies, if any.
        entry_point_args: Optional list of strings. Defaults to None.
            Command line arguments to pass to the `entry_point` program.
        docker_image_build_bucket: Optional string. Cloud storage bucket name.
        called_from_notebook: Boolean. True if the API is run in a
            notebook environment.
        docker_parent_image: Optional parent Docker image to use.
            Defaults to None.
    Raises:
        ValueError: if any of the inputs is invalid.
    """
    _validate_files(entry_point, requirements_txt)
    _validate_other_args(
        entry_point_args,
        docker_image_build_bucket,
        called_from_notebook,
    )


def _validate_files(entry_point, requirements_txt):
    """Validates all the file path params."""
    cwd = os.getcwd()
    if entry_point is not None and (
        not os.path.isfile(os.path.join(cwd, entry_point))):
        raise ValueError(
            "Invalid `entry_point`. "
            "Expected a relative path in the current directory tree. "
            "Received: {}".format(entry_point)
        )

    if requirements_txt is not None and (
        not os.path.isfile(os.path.join(cwd, requirements_txt))
    ):
        raise ValueError(
            "Invalid `requirements_txt`. "
            "Expected a relative path in the current directory tree. "
            "Received: {}".format(requirements_txt)
        )

    if entry_point is not None and (
        not (entry_point.endswith("py") or entry_point.endswith("ipynb"))
    ):
        raise ValueError(
            "Invalid `entry_point`. "
            "Expected a python file or an iPython notebook. "
            "Received: {}".format(entry_point)
        )


def _validate_other_args(
    args, docker_image_build_bucket, called_from_notebook
):
    """Validates all non-file/distribution strategy args."""

    if args is not None and not isinstance(args, list):
        raise ValueError(
            "Invalid `entry_point_args` input. "
            "Expected None or a list. "
            "Received {}.".format(str(args))
        )

    if called_from_notebook and docker_image_build_bucket is None:
        raise ValueError(
            "Invalid `docker_config.image_build_bucket` input. "
            "When `run` API is used within a python notebook, "
            "`docker_config.image_build_bucket` is expected to be specifed. We "
            "will use the bucket name in Google Cloud Storage/Build services "
            "for Docker containerization. Received {}.".format(
                str(docker_image_build_bucket)
            )
        )