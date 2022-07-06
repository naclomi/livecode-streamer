import shutil

class RendererPlugin(object):
    @classmethod
    def canHandleURI(cls, in_filename):
        return False

    @classmethod
    def priority(cls, in_filename):
        return float("-inf")

    def __init__(self, in_filename, out_filename):
        self.in_filename = in_filename
        self.out_filename = out_filename

    def render(self):
        return []


class CopyRenderer(RendererPlugin):
    @classmethod
    def canHandleURI(cls, in_filename):
        return True

    def render(self):
        shutil.copy(self.in_filename, self.out_filename)
        return [self.out_filename]