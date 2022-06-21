import importlib
import traceback

plugin_module_names = [
    "renderer", "pygment_renderer", "nbconvert_renderer"
]
plugin_modules = {}

for module_name in plugin_module_names:
    try:
        module = importlib.import_module("."+module_name, package="renderers")
        plugin_modules[module_name] = module
    except Exception:
        traceback.print_exc()

renderers = plugin_modules["renderer"].get_all_renderers()

def get_renderer(in_filename, out_filename):
    possibilities = []
    for renderer in renderers:
        try:
            if renderer.canHandleFile(in_filename):
                possibilities.append((renderer.priority(in_filename), renderer))
        except Exception:
            traceback.print_exc()
    if len(possibilities) == 0:
        return None
    possibilities.sort(key=lambda tup: tup[0])
    return possibilities[-1][1](in_filename, out_filename)

