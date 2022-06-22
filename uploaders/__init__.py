import importlib
import traceback

plugin_module_names = [
    "uploader", "ssh"
]
plugin_modules = {}

for module_name in plugin_module_names:
    try:
        module = importlib.import_module("."+module_name, package="uploaders")
        plugin_modules[module_name] = module
    except Exception:
        traceback.print_exc()

uploaders = plugin_modules["uploader"].get_all_uploaders()

def get_uploader(uri):
    possibilities = []
    for uploader in uploaders:
        try:
            if uploader.canHandleURI(uri):
                possibilities.append((uploader.priority(uri), uploader))
        except Exception:
            traceback.print_exc()
    if len(possibilities) == 0:
        return None
    possibilities.sort(key=lambda tup: tup[0])
    return possibilities[-1][1]