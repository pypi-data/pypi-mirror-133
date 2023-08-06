import cProfile, pstats
from functools import wraps, partial


def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parameterized
def pprof(f, sort_by="ncalls"):
    @wraps(f)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = f(*args, **kwargs)
        profiler.disable()
        print_stats(profiler, sort_by=sort_by)
        return result

    return wrapper


def print_stats(profiler, sort_by="ncalls"):
    stats = pstats.Stats(profiler)
    stats.sort_stats(sort_by)
    stats.print_stats()
