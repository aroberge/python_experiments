This code is just a proof of concept illustrating how one could
support new constructs (including new keywords) in Python code.

Version 0
----------

This version contains a single file and was my starting point,
essentially what was the first
version used in Reeborg's World.  The file shows how one can
transform some source code so that
instances of

        repeat n:

where "n" evaluates as an integer, are replaced by

        for VAR_i in range(n):

Version 1
---------

This version contains 3 files.  One is the code converter, essentially
identical to the one file from the first version.  Another is a code sample
to be tested.  The third contains an "import hook".  The idea is that
when a module is imported, instead of the standard Python importer,
the custom "import hook" is first called and can decide to handle (and transform)
the code, or just pass it along to the standard Python importer.

Version 2
---------

This version is similar to the previous one.  The main change is that,
instead of having a hard-coded name for the code transformer, it is read
from the source code of the file to be imported.

Version 3
---------

This version handles multiple converters which can be chained.
The code for the converters has been changed from the original:
instead of some simple string substitutions, it uses the
tokenize module to perform changes.  This ensures that
code within comments (including docstrings) is unaffected which would
be useful to preserve docstrings used in Python's help().

Version 4
---------

This version is more robust in being able to deal with extra spaces
in "from `__experimental__` import" and does not require this line
to be the first one in the script; it is also capable of running a script
as though it was run from the command line instead of just when
it is imported.

To see it in action, execute:

    python import_experimental.py test

which will execute test.py after converting it from its non-standard
syntax.

Version 5
---------

I've replaced `__experimental__` by `__nonstandard__`.
In this version, I implemented a French equivalent Python syntax.

To see it in action, first, have a look at test.py and then execute:

    python import_nonstandard.py test

Alternatively, execute:

    python test_import.py

The entire content of test_import.py is:

    import import_nonstandard
    import test


By importing `import_nonstandard`, we modify the way that future modules
are imported which, in this case, means that test.py will be have its
"French Python" syntax translated to the normal Python syntax prior to
being executed.

Version 6
---------

This simply implement a "where" clause, which I would have liked to see
used for type hinting as mentioned on my blog
http://aroberge.blogspot.ca/2015/01/type-hinting-in-python-focus-on.html

Version 7
---------

This demonstrate how to implement an increment operator (++) such that
any line of the form 

    identifier ++   # optional comment 

would be transformed to become

    identifier += 1

For demonstration, have a look at the content of test_increment.py and then execute the following:

    python import_experimental.py test_increment

