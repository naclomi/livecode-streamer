import plugins

plugin_classes = []
def get_uploader(uri):
    global plugin_classes
    if len(plugin_classes) == 0:
        plugin_classes += plugins.load_plugins(__name__, "UploaderPlugin", [
            "uploader", "ssh", "azure", "aws", "git", "localhost"
        ])
    return plugins.get_plugin(uri, plugin_classes)
