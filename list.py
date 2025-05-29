# 1. Creating a list
numbers = [10, 20, 30, 40, 50]
print("Original List:", numbers)

# 2. Accessing elements
print("First element:", numbers[0])
print("Last element:", numbers[-1])

# 3. Slicing
print("Middle elements:", numbers[1:4])

# 4. Updating an element
numbers[2] = 35
print("After update:", numbers)

# 5. Adding elements
numbers.append(60)
print("After append:", numbers)

numbers.insert(2, 25)
print("After insert at index 2:", numbers)

# 6. Removing elements
numbers.remove(25)
print("After remove 25:", numbers)

popped = numbers.pop()
print("Popped value:", popped)
print("After pop:", numbers)

# 7. Searching
print("Index of 40:", numbers.index(40))
print("Count of 20:", numbers.count(20))

# 8. Sorting
numbers.sort()
print("Sorted list:", numbers)

# 9. Reversing
numbers.reverse()
print("Reversed list:", numbers)

# 10. Length
print("Length:", len(numbers))

# 11. Iterating through a list
print("Iterating:")
for num in numbers:
    print(num)

# 12. Checking existence
print("Is 30 in list?", 30 in numbers)

# 13. Copying list
copy_numbers = numbers.copy()
print("Copied list:", copy_numbers)

# 14. Clearing list
copy_numbers.clear()
print("Cleared copy:", copy_numbers)

# 15. Nested lists
nested = [[1, 2], [3, 4], [5, 6]]
print("Nested list:", nested)
print("Accessing nested item:", nested[1][1])

# 16. List comprehension
squares = [x**2 for x in range(1, 6)]
print("List of squares:", squares)

# 17. Combining two lists
a = [1, 2]
b = [3, 4]
combined = a + b
print("Combined list:", combined)

# 18. Repeating list
repeated = ["Hi"] * 3
print("Repeated list:", repeated)

# 19. Convert tuple to list
tup = (7, 8, 9)
converted = list(tup)
print("Converted from tuple:", converted)

# 20. Filtering using list comprehension
even_numbers = [x for x in numbers if x % 2 == 0]
print("Even numbers from list:", even_numbers)
