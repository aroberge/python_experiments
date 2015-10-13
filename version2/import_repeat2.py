
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
        lines = source.split('\n')
        first_line = lines[0]

        # the following could be done more efficiently using a
        # carefully written regular expression and the re module ...
        if first_line.startswith("from __experimental__ import"):
            first_line = first_line.replace("from __experimental__ import", "").strip()

            # first_line should now be 'repeat_keyword'
            mod_name = __import__(first_line)
            source = mod_name.transform_source_code('\n'.join(lines[1:]))

            # create new module
            module = imp.new_module(name)
            exec(source, module.__dict__)
            sys.modules[name] = module
            return module
        return None

sys.meta_path = [TestImporter()]

if __name__ == '__main__':
    import math
    assert math.pi != 0   # ensures import works correctly
    import repeat_sample2

    repeat_sample2.draw_square()
