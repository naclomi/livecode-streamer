import logging
import subprocess
import re
import traceback
import importlib

def load_plugins(package, base_class, plugin_module_names):
    plugin_modules = {}
    for module_name in plugin_module_names:
        try:
            module = importlib.import_module("."+module_name, package=package)
            plugin_modules[module_name] = module
        except Exception:
            logging.info(traceback.format_exc())

    base_class = getattr(plugin_modules[plugin_module_names[0]], base_class)

    # from https://stackoverflow.com/a/5883218
    subclasses = set()
    work = [base_class]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses

def get_plugin(uri, plugins):
    possibilities = []
    for plugin in plugins:
        try:
            if plugin.canHandleURI(uri):
                possibilities.append((plugin.priority(uri), plugin))
        except Exception:
            logging.info(traceback.format_exc())
    if len(possibilities) == 0:
        return None
    possibilities.sort(key=lambda tup: tup[0])
    return possibilities[-1][1]

def command_exists(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            return False
    except Exception:
        logging.info(traceback.format_exc())
        return False
    return True

def command_expects(cmd, pattern):
    try:
        result = subprocess.run(cmd, capture_output=True)
        if re.match(result.stdout.decode(), pattern) is None:
            return False
    except Exception:
        logging.info(traceback.format_exc())
        return False
    return True
