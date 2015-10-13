
import imp
import sys


class TestImporter(object):

    def find_module(self, name, path=None):
        self.module_info = imp.find_module(name)
        return self

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        path = self.module_info[1]
        module = None

        if path is not None:
            with open(path) as source_file:
                module = self.convert_experimental(name, source_file.read())
        if module is None:
            module = imp.load_module(name, *self.module_info)
        return module

    def convert_experimental(self, name, source):
        if "repeat_keyword" in source:
            import repeat_keyword
            module = imp.new_module(name)
            exec(repeat_keyword.transform_source_code(source), module.__dict__)
            sys.modules[name] = module
            return module
        return None

sys.meta_path = [TestImporter()]

if __name__ == '__main__':
    import math
    assert math.pi != 0
    import repeat_sample1

    repeat_sample1.draw_square()
