import os
import __main__


class ResourceLocation:
    def __init__(self, path):
        self.path = os.path.join(os.path.dirname(__main__.__file__), path)

    def getFullPath(self):
        return os.path.abspath(self.path)