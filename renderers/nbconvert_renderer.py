import traceback

import nbformat
import nbconvert
import jinja2
from renderers.renderer import RendererPlugin

class NbconvertRenderer(RendererPlugin):
    @classmethod
    def canHandleURI(cls, in_filename):
        try:
            with open(in_filename, "r") as f:
                raw_nb = f.read()
                nbformat.reads(raw_nb, as_version=4)
            return True
        except Exception:
            # TODO: log error message
            return False

    @classmethod
    def priority(cls, in_filename):
        return 10


    def render(self):
        with open(self.in_filename, "r") as f:
            raw_nb = f.read()
            nb = nbformat.reads(raw_nb, as_version=4)
        with open(self.out_filename, "w") as f:

            # TODO: use a programmatic template to navigate to bottom of the page
            html_exporter = nbconvert.HTMLExporter(template_name = 'classic')

            (body, resources) = html_exporter.from_notebook_node(nb)
            f.write(body)
        return [self.out_filename]

def renderer(f):
    return ""


