# 1. Creating a tuple
fruits = ("apple", "banana", "cherry", "date")
print("Original tuple:", fruits)

# 2. Accessing elements
print("First fruit:", fruits[0])
print("Last fruit:", fruits[-1])

# 3. Slicing a tuple
print("Middle fruits:", fruits[1:3])

# 4. Iterating through a tuple
print("Iterating through tuple:")
for fruit in fruits:
    print(fruit)

# 5. Tuple length
print("Length of tuple:", len(fruits))

# 6. Checking existence
print("Is 'banana' in tuple?", "banana" in fruits)

# 7. Tuple with mixed data types
mixed = ("Alice", 25, 5.5, True)
print("Mixed tuple:", mixed)

# 8. Nested tuples
nested = (fruits, mixed)
print("Nested tuple:", nested)

# 9. Repeating elements
repeat = ("Hi",) * 3
print("Repeated tuple:", repeat)

# 10. Concatenation
combined = fruits + ("elderberry", "fig")
print("Concatenated tuple:", combined)

# 11. Tuple unpacking
person = ("Bob", 30, "Engineer")
name, age, profession = person
print("Unpacked values:", name, age, profession)

# 12. Tuple methods
numbers = (1, 2, 3, 2, 4, 2)
print("Count of 2:", numbers.count(2))
print("Index of 4:", numbers.index(4))

# 13. Convert list to tuple
lst = ["x", "y", "z"]
tup_from_list = tuple(lst)
print("Tuple from list:", tup_from_list)

# 14. Use tuple as a dictionary key
location = {(10, 20): "Park", (30, 40): "Mall"}
print("Location at (10, 20):", location[(10, 20)])
