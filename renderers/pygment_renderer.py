import os

import pygments
import pygments.lexers
import pygments.util
import pygments.formatters

from renderers.renderer import RendererPlugin

class PygmentsRenderer(RendererPlugin):
    @classmethod
    def canHandleURI(cls, in_filename):
        try:
            pygments.lexers.get_lexer_for_filename(in_filename)
            return True
        except pygments.util.ClassNotFound:
            return False

    @classmethod
    def priority(cls, in_filename):
        return 0

    def __init__(self, in_filename, out_filename):
        super().__init__(in_filename, out_filename)
        self.lexer = pygments.lexers.get_lexer_for_filename(in_filename)
        self.formatter = pygments.formatters.HtmlFormatter(style='colorful')

    def render(self):
        with open(self.in_filename, "r") as f:
            code = f.read()
        with open(self.out_filename, "w") as f:
            code_seg = pygments.highlight(code, self.lexer, self.formatter)
            style_seg = self.formatter.get_style_defs()
            html_code = """
                <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
                   "http://www.w3.org/TR/html4/strict.dtd">
                <html>
                <head>
                    <title>{:}</title>
                    <meta http-equiv="content-type" content="text/html; charset=None">
                    <style type="text/css">
                        {:}
                    </style>
                </head>
                <body>
                    {:}
                    <script type="text/javascript">
                        window.scrollTo(0,document.body.scrollHeight);
                        window.onbeforeunload = function () {{
                            window.scrollTo(0,document.body.scrollHeight);
                        }}
                    </script>
                </body>
                </html>
            """.format(os.path.basename(self.in_filename), style_seg, code_seg)
            f.write(html_code)
        return [self.out_filename]

def renderer(f):
    return ""


