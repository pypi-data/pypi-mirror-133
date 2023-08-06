"""Google Cloud Build client."""

import logging
import google.auth

from src.python.mlenv_cloud.utils import gcs

from google.protobuf import duration_pb2
from google.cloud.devtools import cloudbuild_v1

_BUILD_BUCKET = "news-ml-dev"
_CONTAINER_NAME = "us-central1-docker.pkg.dev/news-ml-257304/mlenv/jupyter:v1"
_BUILD_TIMEOUT = 900


def get_client():
    """Authenticates with local credentials."""
    _, project_id = google.auth.default()
    client = cloudbuild_v1.services.cloud_build.CloudBuildClient()
    return project_id, client


def build_steps(container_name, timeout=600):
    """Build steps to be executed by Google Cloud Build."""
    if not container_name:
        raise ValueError("Invalid container name")
    logging.info('Building container: {} Timeout: {} seconds'.format(container_name, timeout))
    duration = duration_pb2.Duration()
    duration.seconds = timeout
    steps = [
        {
            "name": "gcr.io/cloud-builders/docker",
            "args": [
                "build", "-t", container_name, "--file=./Dockerfile", "."],
            "timeout": duration,
        },
        {
            "name": "gcr.io/cloud-builders/docker",
            "args": [
                "push", container_name]
        },
    ]
    return steps


def build_storage_source(bucket, object_):
    """Create a .tgz file which includes Dockerfile and dependencies. Upload it to GCS bucket"""

    storage_source = cloudbuild_v1.StorageSource(
        {
            "bucket": bucket,
            "object_": object_
        }
    )
    return storage_source


def build_request(bucket, object_):
    """Create and execute a simple Google Cloud Build configuration,
    print the in-progress status and print the completed status."""

    # Authorize the client with Google defaults
    project_id, client = get_client()
    build = cloudbuild_v1.Build()
    print("Build request {} {} {}".format(project_id, bucket, object_))
    storage_source = build_storage_source(bucket, object_)
    # The following build steps will output "hello world"
    # For more information on build configuration, see
    # https://cloud.google.com/build/docs/configuring-builds/create-basic-configuration
    build.source = cloudbuild_v1.Source(
        {
            "storage_source": storage_source,
        }
    )
    build.steps = build_steps(container_name=_CONTAINER_NAME, timeout=600)
    operation = client.create_build(project_id=project_id, build=build, timeout=_BUILD_TIMEOUT)
    # Print the in-progress operation
    return operation

"""
    print("IN PROGRESS:")
    logging.info(operation.metadata)

    result = operation.result()
    # Print the completed status
    print("RESULT:", result.status)
    
"""

if __name__ == "__main__":
    tmp_file = gcs.generate_random_build_filename()
    gcs.compress_folder_to_tgz(
        "/Users/gogasca/Documents/Development/swe/mlenv/src/python/mlenv/core/tests/samples", tmp_file)
    gcs.copy_local_file_to_bucket(tmp_file, _BUILD_BUCKET, "builds")
    remote_path = gcs.remote_build_path("builds", tmp_file) # Example: "source/1640509283.923616-66b513c5.tgz"
    build_request(_BUILD_BUCKET, remote_path)
