import time

def timerfunc(func):
    """A timer decorator to time execution of function

    Args:
        func: Input function
    Returns:
        modified_func: 
    """
    def function_timer(*args, **kwargs):
        """A nested function for timing other functions.
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        print(f"The runtime for {func.__name__} took {runtime} seconds to complete.")

        return value
    return function_timer