from __experimental__ import repeat_keyword, function_keyword


def normal_syntax():
    '''Creates the list [4, 4, 4] by using the normal Python syntax,
       with a for loop and a lambda-defined function.
    '''
    res = []
    g = lambda x: x**2
    for _ in range(3):
        res.append(g(2))
    return res


def experimental_syntax():
    '''Creates the list [4, 4, 4] by using an experimental syntax
       with the keywords "repeat" and "function", otherwise
       using the same algorithm as the function called "normal_syntax".
    '''
    res = []
    g = function x: x**2
    repeat 3:
        res.append(g(2))
    return res


if __name__ == '__main__':
    if normal_syntax() == experimental_syntax():
        print("Success")
    else:
        print("Failure")
