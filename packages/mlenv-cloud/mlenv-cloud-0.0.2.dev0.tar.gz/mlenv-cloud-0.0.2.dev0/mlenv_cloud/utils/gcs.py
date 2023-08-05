"""utils for file operations."""

import logging
import os
import tempfile
import traceback
import subprocess

from google.cloud import storage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_NUM_OF_RETRIES = 3


def display_file_structure():
    print(os.getcwd())
    print(os.listdir("../core"))


def generate_random_build_filename():
    tf = tempfile.NamedTemporaryFile(prefix="build")
    return tf.name + ".tgz"


def remote_build_path(gcs_path, local_file):
    """Builds the remote directory location in GCS."""
    local_file = os.path.basename(local_file)
    return os.path.join(gcs_path, *local_file.split("/"))


def compress_folder_to_tgz(path, output_filename):
    """Generate a .tgz file from a folder path.

    Args:
        path: Local folder path.
        output_filename: The .tar.gz (.tgz) file to be used.

    Returns:
        Final .tgz file name.
    """
    try:
        print("Compressing folder: {} to: {}".format(path, output_filename))
        # https://stackoverflow.com/a/5696001/260826
        cmd = ['tar', '-czvf', output_filename, '-C', path, '.']
        output = subprocess.check_output(cmd).decode("utf-8").strip()
        print(output)
        list_tgz_file_contents(output_filename)
    except subprocess.CalledProcessError:
        print(f"E: {traceback.format_exc()}")


def list_tgz_file_contents(path):
    """List a .tgz file contents without extracting."""
    try:
        print("Local directory: {}".format(path))
        cmd = ['tar', '-ztvf', path]
        output = subprocess.check_output(cmd).decode("utf-8").strip()
        print(output)
    except subprocess.CalledProcessError:
        print(f"E: {traceback.format_exc()}")


def copy_local_file_to_bucket(local_file, destination_bucket_name, gcs_path):
    """Copies a blob from one bucket to another with a new name."""
    # local_file = "your-local-file-name"
    # destination_bucket_name = "destination-bucket-name"
    # gcs_path = "destination-object-name"

    storage_client = storage.Client()
    destination_bucket = storage_client.bucket(destination_bucket_name)

    assert os.path.isfile(local_file)
    # https://stackoverflow.com/a/49961041
    remote_path = remote_build_path(gcs_path, local_file)
    print("Remote path: {}".format(remote_path))
    blob = destination_bucket.blob(remote_path)
    blob.upload_from_filename(local_file, num_retries=_NUM_OF_RETRIES)
