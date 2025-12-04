def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Running function: {func.__name__}")
        result = func(*args, **kwargs)
        print("Completed.")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

output = add(5, 7)
print("Result =", output)
