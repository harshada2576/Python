import time

def timer(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print("Time taken:", end - start, "seconds")
    return wrapper

@timer
def task():
    for i in range(500000):
        pass

task()
