import subprocess
import re
import traceback

import keyring
import json

class UploaderPlugin(object):
    @classmethod
    def canHandleURI(cls, uri):
        return False

    @classmethod
    def priority(cls, uri):
        return float("-inf")

    @classmethod
    def configure(cls, uri, forced=False):
        return None

    def __init__(self, uri, force_configuration=False):
        self.uri = uri

        config_key = "{:}/{:}".format(type(self).__name__, uri)
        self.config = json.loads(keyring.get_password("livecode-streamer", config_key))
        if force_configuration or self.config is None:
            self.config = type(self).configure(uri, force_configuration, self.config if self.config is not None else {})
            if len(self.config) > 0:
                keyring.set_password("livecode-streamer", config_key, json.dumps(self.config))

    def uploadDirectory(self, path):
        pass

def command_exists(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            return False
    except Exception:
        traceback.print_exc()
        return False
    return True

def command_expects(cmd, pattern):
    try:
        result = subprocess.run(cmd, capture_output=True)
        if re.match(result.stdout.decode(), pattern) is None:
            return False
    except Exception:
        traceback.print_exc()
        return False
    return True


def get_all_uploaders():
    # from https://stackoverflow.com/a/5883218
    subclasses = set()
    work = [UploaderPlugin]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses
