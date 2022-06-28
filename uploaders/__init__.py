import plugins

uploaders = plugins.load_plugins(__name__, "UploaderPlugin", [
    "uploader", "ssh", "git"
])

def get_uploader(uri):
    return plugins.get_plugin(uri, uploaders)
