import time

def benchmark(func, *args, **kwargs):

    result, runtime = func(
        *args,
        **kwargs
    )

    return {
        "result": result,
        "runtime": runtime
    }