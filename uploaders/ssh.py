import os
import subprocess
import traceback

from uploaders.uploader import UploaderPlugin, command_exists, command_expects

class ScpUploader(UploaderPlugin):
    @classmethod
    def canHandleURI(cls, uri):
        if ":" not in uri:
            return false
        return command_expects(["scp"], "usage: scp")

    @classmethod
    def priority(cls, uri):
        return 10

    def uploadDirectory(self, path):
        subprocess.run(["scp", "-r", os.path.join(path, "*"), os.path.join(self.uri,"")])

class RsyncUploader(UploaderPlugin):
    @classmethod
    def canHandleURI(cls, uri):
        if ":" not in uri:
            return false
        return command_exists(["rsync", "--version"])

    @classmethod
    def priority(cls, uri):
        return 20

    def uploadDirectory(self, path):
        subprocess.run(["rsync", "-r", os.path.join(path, "*"), os.path.join(self.uri,"")])

class WslRsyncUploader(UploaderPlugin):
    @classmethod
    def canHandleURI(cls, uri):
        if ":" not in uri:
            return false
        return command_exists(["wsl", "rsync", "--version"])

    @classmethod
    def priority(cls, uri):
        return 21

    def uploadDirectory(self, path):
        subprocess.run(["wsl", "rsync", "-r", "$(wslpath -a '%s')" % os.path.join(path, ""), os.path.join(self.uri,"")])

