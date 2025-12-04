def repeat(times):
    def decorator(func):
        def wrapper():
            for _ in range(times):
                func()
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("Hello!")

hello()
