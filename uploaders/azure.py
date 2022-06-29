import sys
import os

from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceExistsError

from uploaders.uploader import UploaderPlugin
class AzureBlobStorageUploader(UploaderPlugin):
    URI_PREFIX = "azure://"

    @classmethod
    def canHandleURI(cls, uri):
        return uri.lower().startswith(cls.URI_PREFIX)

    @classmethod
    def priority(cls, uri):
        return 30

    @classmethod
    def configure(cls, uri, forced, old_config):
        if uri.startswith(cls.URI_PREFIX):
            account_name = uri[len(cls.URI_PREFIX):]
        else:
            account_name = uri
        connection_string = input("Please provide connection string for storage account '{:}':\n".format(account_name))
        if connection_string.strip() == "":
            print("No connection details provided, aborting")
            sys.exit(1)
        return {"connection_string": connection_string}

    def initUploader(self):
        self.service_client = BlobServiceClient.from_connection_string(self.config["connection_string"])
        self.container_client = self.service_client.get_container_client("$web")
        try:
            self.container_client.create_container()
        except ResourceExistsError:
            pass


    def uploadFiles(self, files):
        for file in files:
            blob_client = self.service_client.get_blob_client(container="$web", blob=os.path.basename(file))
            with open(file, "rb") as data:
                blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(
                    content_type="text/html"))
