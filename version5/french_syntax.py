from io import StringIO
import tokenize


def transform_source_code(text):
    '''Input text is assumed to contain some French equivalent words to
       normal Python keywords and a few builtin functions.
       These are transformed into normal Python keywords and functions.
    '''
    # continue, def, global, lambda, nonlocal remain unchanged by choice

    dictionary = {'Faux': 'False', 'Aucun': 'None', 'Vrai': 'True',
                   'et': 'and', 'comme': 'as', 'affirme': 'assert',
                   'sortir': 'break', 'classe': 'class', 'élimine': 'del',
                   'ousi': 'elif', 'autrement': 'else', 'exception': 'except',
                   'finalement': 'finally', 'pour': 'for', 'de': 'from',
                   'si': 'if', 'importe': 'import', 'dans': 'in', 'est': 'is',
                   'non': 'not', 'ou': 'or', 'passe': 'pass',
                   'soulever': 'raise', 'retourne': 'return', 'essayer': 'try',
                   'pendant': 'while', 'avec': 'with', 'céder': 'yield',
                   'imprime': 'print', 'intervalle': 'range'}

    toks = tokenize.generate_tokens(StringIO(text).readline)
    result = []
    for toktype, tokvalue, _, _, _ in toks:
        if toktype == tokenize.NAME and tokvalue in dictionary:
            result.append((toktype, dictionary[tokvalue]))
        else:
            result.append((toktype, tokvalue))
    return tokenize.untokenize(result)
