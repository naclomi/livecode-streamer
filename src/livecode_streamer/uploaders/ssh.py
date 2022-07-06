import os
import subprocess
import traceback
import shlex

from uploaders.uploader import UploaderPlugin
from plugins import command_exists, command_expects


class SshUploaderPlugin(UploaderPlugin):
    COMMAND_NAME = ""
    EXISTS_FLAGS = []
    UPLOAD_FLAGS = []
    PRIORITY = 10

    CONFIG_FLAGS_PLACEHOLDER = object()

    @classmethod
    def canHandleURI(cls, uri):
        if cls.COMMAND_NAME == "":
            return False
        if ":" not in uri:
            return False
        return command_exists([cls.COMMAND_NAME] + cls.EXISTS_FLAGS)

    @classmethod
    def priority(cls, uri):
        return cls.PRIORITY

    @classmethod
    def configure(cls, uri, forced, old_config):
        if forced:
            if "flags" in old_config:
                default = old_config["flags"]
                old_flags = " [{:}]".format(old_config["flags"])
            else:
                default = ""
                old_flags = ""
            flags = input("Please enter command-line flags for {:}{:}: ".format(cls.COMMAND_NAME, old_flags))
            if flags == "":
                flags = default
            return {"flags": flags}
        else:
            return {}

    def uploadFiles(self, files):
        if "flags" in self.config:
            cfg_flags = shlex.split(self.config["flags"])
        else:
            cfg_flags = []

        final_cmd = [self.COMMAND_NAME]
        for flag in self.UPLOAD_FLAGS:
            if flag is self.CONFIG_FLAGS_PLACEHOLDER:
                final_cmd += cfg_flags
            elif "{LOCAL_FILE}" in flag:
                for file in files:
                    final_cmd.append(flag.format(LOCAL_FILE=file))
            else:
                final_cmd.append(flag.format(REMOTE_URI=os.path.join(self.uri,"")))
        subprocess.run(final_cmd)

class ScpUploader(SshUploaderPlugin):
    COMMAND_NAME = "scp"
    UPLOAD_FLAGS = [
        SshUploaderPlugin.CONFIG_FLAGS_PLACEHOLDER,
        "{LOCAL_FILE}",
        "{REMOTE_URI}"]
    PRIORITY = 10

    @classmethod
    def canHandleURI(cls, uri):
        if ":" not in uri:
            return False
        return command_expects(["scp"], "usage: scp")

class RsyncUploader(SshUploaderPlugin):
    COMMAND_NAME = "rsync"
    EXISTS_FLAGS = ["--version"]
    UPLOAD_FLAGS = [
        SshUploaderPlugin.CONFIG_FLAGS_PLACEHOLDER,
        "{LOCAL_FILE}",
        "{REMOTE_URI}"]
    PRIORITY = 20

class WslRsyncUploader(SshUploaderPlugin):
    COMMAND_NAME = "wsl"
    EXISTS_FLAGS = ["rsync", "--version"]
    UPLOAD_FLAGS = [
        "rsync",
        SshUploaderPlugin.CONFIG_FLAGS_PLACEHOLDER,
        "$(wslpath -a '{LOCAL_FILE}')",
        "{REMOTE_URI}"]
    PRIORITY = 21

