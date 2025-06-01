# 1. Basic for loop with a list
print("1. Iterating over a list:")
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(fruit)

# 2. Iterating over a string
print("\n2. Iterating over a string:")
for char in "Python":
    print(char)

# 3. Using range()
print("\n3. Using range():")
for i in range(5):
    print(i)

# 4. Custom start and step in range()
print("\n4. range(start, stop, step):")
for i in range(2, 10, 2):
    print(i)

# 5. Iterating over a tuple
print("\n5. Iterating over a tuple:")
colors = ("red", "green", "blue")
for color in colors:
    print(color)

# 6. Iterating over a dictionary
print("\n6. Iterating over a dictionary:")
person = {"name": "Alice", "age": 30, "city": "Paris"}
for key in person:
    print(f"{key}: {person[key]}")

# 7. Iterating over dictionary items
print("\n7. Dictionary items:")
for key, value in person.items():
    print(f"{key} = {value}")

# 8. Iterating over a set
print("\n8. Iterating over a set:")
unique_numbers = {1, 2, 3, 4}
for num in unique_numbers:
    print(num)

# 9. Using break
print("\n9. Using break:")
for i in range(10):
    if i == 5:
        print("Breaking at 5")
        break
    print(i)

# 10. Using continue
print("\n10. Using continue:")
for i in range(5):
    if i == 2:
        print("Skipping 2")
        continue
    print(i)

# 11. Using else with for
print("\n11. Using else with for:")
for i in range(3):
    print(i)
else:
    print("Loop completed without break")

# 12. Else with break
print("\n12. Else skipped due to break:")
for i in range(5):
    if i == 3:
        break
    print(i)
else:
    print("This won't print due to break")

# 13. Nested for loops
print("\n13. Nested for loops (Multiplication table):")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} * {j} = {i*j}")
    print("-----")

# 14. Using enumerate
print("\n14. Using enumerate:")
animals = ['cat', 'dog', 'elephant']
for index, animal in enumerate(animals):
    print(f"{index}: {animal}")

# 15. Using zip
print("\n15. Using zip:")
names = ["John", "Jane", "Jim"]
ages = [25, 30, 22]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# 16. List comprehension with for loop
print("\n16. List comprehension:")
squares = [x**2 for x in range(6)]
print("Squares:", squares)

# 17. Filtering with list comprehension
print("\n17. Filtering even numbers using list comprehension:")
evens = [x for x in range(10) if x % 2 == 0]
print("Evens:", evens)
