import os
import shutil

from typing import List

from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset, Datafile
from easyDataverse.core.exceptions import MissingURLException, MissingCredentialsException


def uploadToDataverse(json_data: str, dataverse_name: str, filenames: List[str] = None) -> str:

    # Get environment variables
    try:
        DATAVERSE_URL = os.environ["DATAVERSE_URL"]

    except KeyError:
        raise MissingURLException

    try:
        API_TOKEN = os.environ["DATAVERSE_API_TOKEN"]
    except KeyError:
        raise MissingCredentialsException

    # Initialize pyDataverse API and Dataset
    api = NativeApi(DATAVERSE_URL, API_TOKEN)
    ds = Dataset()
    ds.from_json(json_data)

    # Finally, validate the JSON
    if ds.validate_json():
        response = api.create_dataset(
            dataverse_name, json_data
        )

        if response.json()["status"] != "OK":
            raise Exception(response.json()["message"])

        # Get response data
        ds_pid = response.json()["data"]["persistentId"]

        if filenames is not None:
            # Upload files if given
            for filename in filenames:
                __uploadFile(
                    filename=filename,
                    ds_pid=ds_pid,
                    api=api
                )

        return ds_pid

    else:
        raise Exception("Could not upload")


def __uploadFile(filename: str, ds_pid: str, api: NativeApi) -> None:
    """Uploads any file to a dataverse dataset.
    Args:
        filename (String): Path to the file
        ds_pid (String): Dataset permanent ID to upload.
        api (API): API object which is used to upload the file
    """

    # Check if its a dir
    if os.path.isdir(filename):
        shutil.make_archive("contents", 'zip', filename)
        filename = "contents.zip"

    df = Datafile()
    df.set({"pid": ds_pid, "filename": filename})
    api.upload_datafile(ds_pid, filename, df.json())
