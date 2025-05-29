# 1. Creating a dictionary
student = {
    "name": "Alice",
    "age": 21,
    "grade": "A",
    "courses": ["Math", "Science"]
}

print("Initial Dictionary:", student)

# 2. Accessing values
print("Name:", student["name"])
print("Courses:", student.get("courses"))

# 3. Adding a new key-value pair
student["email"] = "alice@example.com"
print("After adding email:", student)

# 4. Updating existing value
student["age"] = 22
print("After updating age:", student)

# 5. Deleting a key-value pair
del student["grade"]
print("After deleting grade:", student)

# 6. Using pop() to remove and get a value
email = student.pop("email")
print("Popped email:", email)
print("After popping email:", student)

# 7. Checking for key existence
print("Is 'name' in dictionary?", "name" in student)

# 8. Iterating over dictionary
print("\nIterating keys and values:")
for key, value in student.items():
    print(key, ":", value)

# 9. Dictionary length
print("Number of items:", len(student))

# 10. Dictionary keys, values, items
print("Keys:", list(student.keys()))
print("Values:", list(student.values()))
print("Items:", list(student.items()))

# 11. Copying a dictionary
student_copy = student.copy()
print("Copied dictionary:", student_copy)

# 12. Clearing the dictionary
student_copy.clear()
print("After clearing copy:", student_copy)

# 13. Nested dictionary
school = {
    "student1": {"name": "Alice", "age": 21},
    "student2": {"name": "Bob", "age": 23}
}
print("Nested Dictionary:", school)

# 14. Dictionary comprehension
squares = {x: x*x for x in range(1, 6)}
print("Dictionary Comprehension (squares):", squares)
