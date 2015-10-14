from __experimental__ import repeat_keyword, function_keyword


def experimental_syntax():
    '''Creates the list [4, 4, 4] by using an experimental syntax
       with the keywords "repeat" and "function"
    '''
    res = []
    g = function x: x**2
    repeat 3:
        res.append(g(2))
    return res


def normal_syntax():
    '''Creates the list [4, 4, 4] by using the normal Python syntax,
        otherwise using the same procedure as the experimental_syntax
        function
    '''
    res = []
    g = lambda x: x**2
    for i in range(3):
        res.append(g(2))
    return res

if __name__ == '__main__':
    if normal_syntax() == experimental_syntax():
        print("Success")
    else:
        print("Failure")
