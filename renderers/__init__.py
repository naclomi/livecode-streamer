import plugins

renderers = plugins.load_plugins(__name__, "RendererPlugin", [
    "renderer", "pygment_renderer", "nbconvert_renderer"
])

def get_renderer(uri):
    return plugins.get_plugin(uri, renderers)

