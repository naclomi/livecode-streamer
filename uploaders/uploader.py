import subprocess
import re
import traceback

class UploaderPlugin(object):
    @classmethod
    def canHandleURI(cls, uri):
        return False

    @classmethod
    def priority(cls, uri):
        return float("-inf")

    def __init__(self, uri):
        self.uri = uri

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
