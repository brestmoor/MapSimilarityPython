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
        print(func.__name__ + " took: " + str(end - start))
        return ret

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