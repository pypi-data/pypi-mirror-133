"""Utilities for Google API client."""

import enum
import os
import sys
from typing import Text, Union
from .. import version
from absl import logging


_TF_CLOUD_USER_AGENT_HEADER = "tf-cloud/" + version.__version__
_POLL_INTERVAL_IN_SECONDS = 30
_LOCAL_CONFIG_PATH = os.path.expanduser(
    "~/.config/tf_cloud/tf_cloud_config.json")
_PRIVACY_NOTICE = """
This application reports technical and operational details of your usage of
Cloud Services in accordance with Google privacy policy, for more information
please refer to https://policies.google.com/privacy. If you wish
to opt-out, you may do so by running
tensorflow_cloud.utils.google_api_client.optout_metrics_reporting().
"""

_TELEMETRY_REJECTED_CONFIG = "telemetry_rejected"
_TELEMETRY_VERSION_CONFIG = "notification_version"

_KAGGLE_ENV_VARIABLE = "KAGGLE_CONTAINER_NAME"
_DL_ENV_PATH_VARIABLE = "DL_PATH"


class ClientEnvironment(enum.Enum):
    """Types of client environment for telemetry reporting."""
    UNKNOWN = 0
    KAGGLE_NOTEBOOK = 1
    HOSTED_NOTEBOOK = 2
    DLVM = 3
    DL_CONTAINER = 4
    COLAB = 5


# TODO(b/176097105) Use get_client_environment_name in tfc.run and cloud_fit
def get_client_environment_name() -> Text:
    """Identifies the local environment where tensorflow_cloud is running.
    Returns:
        ClientEnvironment Enum representing the environment type.
    """
    if _get_env_variable(_KAGGLE_ENV_VARIABLE):
        logging.info("Kaggle client environment detected.")
        return ClientEnvironment.KAGGLE_NOTEBOOK.name

    if _is_module_present("google.colab"):
        logging.info("Detected running in COLAB environment.")
        return ClientEnvironment.COLAB.name

    if _get_env_variable(_DL_ENV_PATH_VARIABLE):
        # TODO(b/171720710) Update logic based resolution of the issue.
        if _get_env_variable("USER") == "jupyter":
            logging.info("Detected running in HOSTED_NOTEBOOK environment.")
            return ClientEnvironment.HOSTED_NOTEBOOK.name

        # TODO(b/175815580) Update logic based resolution of the issue.
        logging.info("Detected running in DLVM environment.")
        return ClientEnvironment.DLVM.name

    # TODO(b/175815580) Update logic based resolution of the issue.
    if _is_module_present("google"):
        logging.info("Detected running in DL_CONTAINER environment.")
        return ClientEnvironment.DL_CONTAINER.name

    logging.info("Detected running in UNKNOWN environment.")
    return ClientEnvironment.UNKNOWN.name


def _is_module_present(module_name: Text) -> bool:
    """Checks if module_name is present in sys.modules.
    Args:
        module_name: Name of the module to look up in the system modules.
    Returns:
        True if module exists, False otherwise.
    """
    return module_name in sys.modules


def _get_env_variable(variable_name: Text) -> Union[Text, None]:
    """Looks up the value of environment varialbe variable_name.
    Args:
        variable_name: Name of the variable to look up in the environment.
    Returns:
        A string representing the varialbe value or None if varialbe is not
        defined in the environment.
    """
    return os.getenv(variable_name)
