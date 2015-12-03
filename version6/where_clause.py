from io import StringIO
import tokenize

sample_in = '''
def twice(i, next):
    where:
        i: int
        next: Function[[int], int]
        return: int
    return next(next(i))
'''

sample_out = '''
def twice (i ,next ):
    return next (next (i ))
'''

variable_in = '''
x = 3
where:
    x: int
y = 4
'''

variable_out = '''
x=3
y=4
'''


def transform_source_code(text):
    '''removes a "where" clause which is identified by the use of "where"
    as an identifier and ends at the first DEDENT (i.e. decrease in indentation)'''
    toks = tokenize.generate_tokens(StringIO(text).readline)
    result = []
    where_clause = False
    for toktype, tokvalue, _, _, _ in toks:
        if toktype == tokenize.NAME and tokvalue == "where":
            where_clause = True
        elif where_clause and toktype == tokenize.DEDENT:
            where_clause = False
            continue

        if not where_clause:
            result.append((toktype, tokvalue))
    return tokenize.untokenize(result)

assert sample_out == transform_source_code(sample_in)
assert variable_out == transform_source_code(variable_in).replace(' ', '')
