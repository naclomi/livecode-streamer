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
        raw_config = keyring.get_password("livecode-streamer", config_key)
        self.config = json.loads(raw_config) if raw_config is not None else None
        if force_configuration or self.config is None:
            self.config = type(self).configure(uri, force_configuration, self.config if self.config is not None else {})
            if len(self.config) > 0:
                keyring.set_password("livecode-streamer", config_key, json.dumps(self.config))

    def uploadDirectory(self, path):
        pass
