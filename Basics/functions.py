from functools import reduce

# 1. Basic function
def greet(name):
    print(f"Hello, {name}!")

# 2. Function with default and keyword arguments
def describe_person(name, age=30, city="New York"):
    print(f"{name} is {age} years old and lives in {city}.")

# 3. Function with return value
def add(a, b):
    return a + b

# 4. Function with *args (variable-length positional arguments)
def sum_all(*numbers):
    return sum(numbers)

# 5. Function with **kwargs (variable-length keyword arguments)
def print_details(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# 6. Recursive function
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

# 7. Lambda function
square = lambda x: x ** 2

# 8. Nested function (function inside another)
def outer_function(msg):
    def inner_function():
        print(f"Inner message: {msg}")
    inner_function()

# 9. Passing function as argument (First-class function)
def apply_function(func, value):
    return func(value)

# 10. Returning a function
def make_multiplier(x):
    def multiplier(n):
        return x * n
    return multiplier

# 11. Using map, filter, reduce with lambda
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
product = reduce(lambda x, y: x * y, numbers)

# 12. Decorators
def decorator_function(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@decorator_function
def say_hello(name):
    print(f"Hello, {name}!")

# --- Function Calls for Demonstration ---
print("\n1. Basic Function:")
greet("Alice")

print("\n2. Default and Keyword Arguments:")
describe_person("Bob")
describe_person("Carol", city="Los Angeles", age=25)

print("\n3. Return Value:")
print(f"Sum: {add(5, 7)}")

print("\n4. *args:")
print(f"Sum of many: {sum_all(1, 2, 3, 4)}")

print("\n5. **kwargs:")
print_details(name="David", age=40, profession="Engineer")

print("\n6. Recursion (Factorial):")
print(f"Factorial of 5: {factorial(5)}")

print("\n7. Lambda Function:")
print(f"Square of 6: {square(6)}")

print("\n8. Nested Function:")
outer_function("This is a nested call")

print("\n9. First-class Function:")
print(f"Result: {apply_function(square, 10)}")

print("\n10. Returning a Function:")
times3 = make_multiplier(3)
print(f"3 x 4 = {times3(4)}")

print("\n11. Map, Filter, Reduce:")
print(f"Squared: {squared}")
print(f"Evens: {evens}")
print(f"Product: {product}")

print("\n12. Decorators:")
say_hello("Eve")
