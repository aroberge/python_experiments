from io import StringIO
import tokenize


def transform_source_code(text):
    '''Replaces instances of

        function ...
    by

        lambda ...

    '''

    function_keyword = 'function'

    if text.count(function_keyword) == 0:
        return text

    toks = tokenize.generate_tokens(StringIO(text).readline)
    result = []
    for toktype, tokvalue, _, _, _ in toks:
        if toktype == tokenize.NAME and tokvalue == function_keyword:
            result.append((tokenize.NAME, 'lambda'))
            continue
        result.append((toktype, tokvalue))
    return tokenize.untokenize(result)


if __name__ == '__main__':
    sample = '''square = function x: x**2'''

    comparison = '''square =lambda x :x **2 '''

    if comparison == transform_source_code(sample):
        print("Transformation done correctly")
    else:
        print("Transformation done incorrectly")
        import difflib
        d = difflib.Differ()
        diff = d.compare(comparison.splitlines(),
                         transform_source_code(sample).splitlines())
        print('\n'.join(diff))
