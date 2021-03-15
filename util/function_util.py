from timeit import default_timer as timer


def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]

    return helper


def timed(func):
    def timed_func(*args):
        start = timer()
        ret = func(*args)
        end = timer()
        print(func.__name__ + " for " + str(args) + " took: " + str(end - start))
        return ret

    timed_func.original_func_name = func.__name__
    return timed_func


def timeit(func):
    start = timer()
    ret = func()
    end = timer()
    print(func.__name__ + " took: " + str(end - start))
    return ret


def timeit(func, args):
    start = timer()
    ret = func(args)
    end = timer()
    print(func.__name__ + " took: " + str(end - start))
    return ret
