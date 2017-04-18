''' A custom Importer making use of the import hook capability

https://www.python.org/dev/peps/pep-0302/

Its purpose is to convert would-be Python module that use non-standard
syntax into a correct form prior to importing them.
'''

# imp is deprecated but I wasn't (yet) able to figure out how to use
# its replacement, importlib, to accomplish all that is needed here.
import imp
import re
import sys

MAIN = False
from_nonstandard = re.compile("(^from\s+__nonstandard__\s+import\s+)")


class ExperimentalImporter(object):
    '''According to PEP 302, an importer only needs two methods:
       find_module and load_module.
    '''

    def find_module(self, name, path=None):
        '''We don't need anything special here, so we just use the standard
           module finder which, if successful,
           returns a 3-element tuple (file, pathname, description).
           See https://docs.python.org/3/library/imp.html for details
        '''
        self.module_info = imp.find_module(name)
        return self

    def load_module(self, name):
        '''Load a module, given information returned by find_module().
        '''

        # According to PEP 302, the following is required
        # if reload() is to work properly
        if name in sys.modules:
            return sys.modules[name]

        path = self.module_info[1]  # see find_module docstring above
        module = None

        if path is not None:   # path=None is the case for some stdlib modules
            with open(path) as source_file:
                module = self.convert_experimental(name, source_file.read())

        if module is None:
            module = imp.load_module(name, *self.module_info)
        return module

    def convert_experimental(self, name, source):
        '''Used to convert the source code, and create a new module
           if one of the lines is of the form

               ^from __nonstandard__ import converter1 [, converter2, ...]

           (where ^ indicates the beginning of a line)
           otherwise returns None and lets the normal import take place.
           Note that this special code must be all on one physical line --
           no continuation allowed by using parentheses or the
           special \ end of line character.

           "converters" are modules which must contain a function

               transform_source_code(source)

           which returns a tranformed source.
        '''
        global MAIN
        lines = source.split('\n')

        for linenumber, line in enumerate(lines):
            if from_nonstandard.match(line):
                break
        else:
            return None  # normal importer will handle this

        # we started with: "from __nonstandard__ import converter1 [,...]"
        line = from_nonstandard.sub(' ', line)
        # we now have: "converter1 [,...]"
        line = line.split("#")[0]    # remove any end of line comments
        converters = line.replace(' ', '').split(',')
        # and now:  ["converter1", ...]

        # drop the "fake" import from the source code
        del lines[linenumber]
        source = '\n'.join(lines)

        for converter in converters:
            mod_name = __import__(converter)
            source = mod_name.transform_source_code(source)

        module = imp.new_module(name)
        # From PEP 302:  Note that the module object must be in sys.modules
        # before the loader executes the module code.
        # This is crucial because the module code may
        # (directly or indirectly) import itself;
        # adding it to sys.modules beforehand prevents unbounded
        # recursion in the worst case and multiple loading in the best.
        sys.modules[name] = module

        if MAIN:  # see below
            module.__name__ = "__main__"
            MAIN = False
        exec(source, module.__dict__)

        return module


sys.meta_path = [ExperimentalImporter()]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # this program was started by
        # $ python import_experimental.py some_script
        # and we will want some_script.__name__ == "__main__"
        MAIN = True
        __import__(sys.argv[1])
