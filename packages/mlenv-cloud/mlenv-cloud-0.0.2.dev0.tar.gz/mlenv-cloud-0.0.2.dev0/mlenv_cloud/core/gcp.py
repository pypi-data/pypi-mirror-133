"""Utilities related to GCP."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import google.auth


def get_project_name():
    """Returns the current GCP project name."""
    # https://google-auth.readthedocs.io/en/latest/reference/google.auth.html
    _, project_id = google.auth.default()
    if project_id is None:
        raise RuntimeError("Could not determine the GCP project id.")

    return project_id
