from __experimental__ import repeat_keyword, function_keyword


def experimental_syntax():
    res = []
    g = function x: x**2
    repeat 3:
        res.append(g(2))
    return res


def normal_syntax():
    res = []
    g = lambda x: x**2
    for i in range(3):
        res.append(g(2))
    return res
