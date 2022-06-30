import plugins

plugin_classes = []
def get_renderer(uri):
    global plugin_classes
    if len(plugin_classes) == 0:
        plugin_classes += plugins.load_plugins(__name__, "RendererPlugin", [
            "renderer", "pygment_renderer", "nbconvert_renderer"
        ])
    return plugins.get_plugin(uri, plugin_classes)
