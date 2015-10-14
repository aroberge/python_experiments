
import imp
import sys

MAIN = False


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
        global MAIN
        lines = source.split('\n')
        first_line = lines[0]

        # the following could be done more efficiently using a
        # carefully written regular expression and the re module ...
        if first_line.startswith("from __experimental__ import"):
            first_line = first_line.replace("from __experimental__ import", "")
            first_line = first_line.replace(' ', '')
            converters = first_line.split(',')
            source = '\n'.join(lines[1:])

            for converter in converters:
                mod_name = __import__(converter)
                source = mod_name.transform_source_code(source)

            module = imp.new_module(name)
            if MAIN:
                module.__name__ = "__main__"
                MAIN = False
            exec(source, module.__dict__)
            sys.modules[name] = module
            return module
        return None

sys.meta_path = [TestImporter()]

if __name__ == '__main__':
    if len(sys.argv) >= 1:
        MAIN = True
        __import__(sys.argv[1])
