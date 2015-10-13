# A proof of concept to show how to replace a fictitious keyword "repeat"


def transform_source_code(text):
    '''Replaces instances of

           repeat n:

    where "n" is an integer, by

           for VAR_i in range(n):

    where VAR_i is a string that does not appear elsewhere
    in the code sample.  This code is not robust and is more
    a proof of concept than anything else.
    '''

    loop_keyword = 'repeat'

    nb = text.count(loop_keyword)
    if nb == 0:
        return text

    var_names = get_unique_variable_names(text, nb)

    processed_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(loop_keyword):

            # remove end of line comment if present
            stripped = stripped.split('#')[0]

            if ':' in stripped:
                stripped = stripped.replace(loop_keyword, '')
                stripped = stripped.replace(':', '')
                index = line.find(loop_keyword)
                try:
                    # instead of simply allowing an int like "3",
                    # let's be a bit more lenient an allow things like
                    #  "(3)"  or "2*4"
                    n = eval(stripped)
                    assert isinstance(n, int)
                    line = '{0}for {1} in range({2}):'.format(
                                ' '*index, var_names.pop(), n)
                except:   # any error leaves line unchanged
                    pass  # This could definitely be improved upon.
        processed_lines.append(line)
    result = '\n'.join(processed_lines)
    return result


def get_unique_variable_names(text, nb):
    '''returns a list of possible variables names that
       are not found in the original text'''
    base_name = 'VAR_'
    var_names = []
    i = 0
    j = 0
    while j < nb:
        tentative_name = base_name + str(i)
        if text.count(tentative_name) == 0:
            var_names.append(tentative_name)
            j += 1
        i += 1
    return var_names

if __name__ == '__main__':
    sample = '''
        repeat 3:  # first loop
            print('VAR_1')
            repeat (2*2):
                pass
    '''

    comparison = '''
        for VAR_2 in range(3):
            print('VAR_1')
            for VAR_0 in range(4):
                pass
    '''

    if comparison == transform_source_code(sample):
        print("Transformation done correctly")
    else:
        print("Transformation done incorrectly")
        print("Expected code:\n", comparison)
        print("\nResult:\n", transform_source_code(sample))
