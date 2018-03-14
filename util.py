
def accepts(*args):
    def decorator(func):
        def wrapper(*fargs, **kwargs):
            for i, arg in enumerate(args):
                if not isinstance(fargs[i], arg):
                    raise TypeError("Uexpected type '%s' for argument %d, expected '%s'" % (type(fargs[i]).__name__, i+1, arg.__name__))
            
            ret_val = func(*fargs, **kwargs)
            return ret_val

        return wrapper

    return decorator

if __name__ == '__main__':
    @accepts(int)
    def foo(bar):
        print(bar)

    foo(0)