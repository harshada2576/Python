# 1. Creating sets
print("1. Creating sets:")
set1 = {1, 2, 3, 4}
set2 = set([3, 4, 5, 6])
empty_set = set()  # not {}

print("set1:", set1)
print("set2:", set2)
print("empty_set:", empty_set)

# 2. Sets automatically remove duplicates
print("\n2. Sets remove duplicates:")
dupe_set = {1, 2, 2, 3, 3, 3}
print("dupe_set:", dupe_set)

# 3. Adding elements
print("\n3. Adding elements:")
set1.add(5)
print("After adding 5:", set1)

# 4. Removing elements
print("\n4. Removing elements:")
set1.remove(2)  # Raises error if element not found
print("After removing 2:", set1)
set1.discard(10)  # Does NOT raise error
print("After discarding 10:", set1)

# 5. Looping through a set
print("\n5. Looping through a set:")
for item in set1:
    print(item)

# 6. Set operations
print("\n6. Set operations:")
print("set1:", set1)
print("set2:", set2)
print("Union:", set1.union(set2))
print("Intersection:", set1.intersection(set2))
print("Difference (set1 - set2):", set1.difference(set2))
print("Symmetric Difference:", set1.symmetric_difference(set2))

# 7. Subset and Superset
print("\n7. Subset and Superset:")
a = {1, 2}
b = {1, 2, 3, 4}
print("a is subset of b:", a.issubset(b))
print("b is superset of a:", b.issuperset(a))

# 8. Copying sets
print("\n8. Copying sets:")
original = {10, 20, 30}
copied = original.copy()
print("Copied set:", copied)

# 9. Set comprehension
print("\n9. Set comprehension:")
squares = {x**2 for x in range(6)}
print("Squares:", squares)

# 10. Using set to remove duplicates from a list
print("\n10. Remove duplicates from list:")
my_list = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(my_list))
print("Unique elements:", unique)

# 11. Clearing a set
print("\n11. Clearing a set:")
s = {1, 2, 3}
s.clear()
print("After clear():", s)

# 12. Frozen set (immutable set)
print("\n12. Frozenset:")
fs = frozenset([1, 2, 3])
print("Frozen set:", fs)
# fs.add(4)  # This would raise an error (frozen sets can't be modified)
