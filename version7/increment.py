''' transform code of the form
name ++
into 
name += 1

Note: this may fail if ++ appears in triple quoted string
followed by '#' and on the same line as the end of the string.

A more robust solution could be implemented using the tokenize module.
'''

def transform_source_code(src):
    newlines = []
    for line in src.splitlines():
        if ('++') in line:
            newlines.append(transform_line(line))
        else:
            newlines.append(line)
    result = '\n'.join(newlines)
    return result

def transform_line(line):
    original = line
    try:
        first, second = line.split("#")[0].split('++')
    except ValueError:
        return original
    # if line is of the form
    # ...identifier...++...
    # where "..." represent optional spaces
    if first.strip().isidentifier() and second.strip() == '':
        return original.replace("++", "+= 1")
    else:
        return original
