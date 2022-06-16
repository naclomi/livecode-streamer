import shutil

class RendererPlugin(object):
    @classmethod
    def canHandleFile(cls, in_filename):
        return False

    @classmethod
    def priority(cls, in_filename):
        return float("-inf")

    def __init__(self, in_filename, out_filename):
        self.in_filename = in_filename
        self.out_filename = out_filename

    def render(self):
        pass


class CopyRenderer(RendererPlugin):
    @classmethod
    def canHandleFile(cls, in_filename):
        return True

    def render(self):
        shutil.copy(self.in_filename, self.out_filename)


def get_all_renderers():
    # from https://stackoverflow.com/a/5883218
    subclasses = set()
    work = [RendererPlugin]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses
