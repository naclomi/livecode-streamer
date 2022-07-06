import sys
import os

import boto3
from uploaders.uploader import UploaderPlugin

class AWSS3Uploader(UploaderPlugin):
    URI_PREFIX = "arn:aws:s3"

    @classmethod
    def canHandleURI(cls, uri):
        return uri.lower().startswith(cls.URI_PREFIX)

    @classmethod
    def priority(cls, uri):
        return 30

    @classmethod
    def configure(cls, uri, forced, old_config):
        print("Please provide credentials for an AWS acocunt with access to the S3 bucket '{:}'.".format(uri))
        print("WARNING: It is STRONGLY recommended you create an AWS account solely for this purpose, which only has permissions to access this bucket and nothing else. Do NOT use your regular AWS login acocunt here.")
        access_key_id = input("Account access key ID: ")
        secret_access_key = input("Secret access key: ")
        if access_key_id.strip() == "" or secret_access_key.strip() == "":
            print("Incomplete connection details provided, aborting")
            sys.exit(1)
        return {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key
        }

    def initUploader(self):
        self.session = boto3.Session(
            aws_access_key_id=self.config["access_key_id"],
            aws_secret_access_key=self.config["secret_access_key"],
        )
        self.s3 = self.session.resource('s3')


    def uploadFiles(self, files):
        bucket_name = self.uri.split(":")[-1]
        for file in files:
            with open(file, "rb") as data:
                self.s3.Bucket(bucket_name).put_object(
                    Key=os.path.basename(file), Body=data, ContentType="text/html")
