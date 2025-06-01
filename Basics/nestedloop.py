# 1. Basic nested for loop
print("1. Basic nested for loop:")
for i in range(3):
    for j in range(2):
        print(f"i = {i}, j = {j}")
    print("---")

# 2. Pattern printing with nested for loop
print("\n2. Pattern printing (stars):")
rows = 4
for i in range(1, rows + 1):
    for j in range(i):
        print("*", end="")
    print()

# 3. Multiplication table using nested loops
print("\n3. Multiplication Table:")
for i in range(1, 4):
    for j in range(1, 6):
        print(f"{i} x {j} = {i*j}", end="\t")
    print()

# 4. Nested while loops
print("\n4. Nested while loops:")
i = 0
while i < 3:
    j = 0
    while j < 2:
        print(f"[{i},{j}]", end=" ")
        j += 1
    print()
    i += 1

# 5. For loop inside a while loop
print("\n5. For inside while:")
k = 0
while k < 2:
    for l in range(3):
        print(f"k = {k}, l = {l}")
    k += 1

# 6. While loop inside a for loop
print("\n6. While inside for:")
for a in range(2):
    b = 0
    while b < 2:
        print(f"a = {a}, b = {b}")
        b += 1

# 7. Working with 2D list (matrix)
print("\n7. Iterating over a 2D list:")
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
for row in matrix:
    for item in row:
        print(item, end=" ")
    print()

# 8. Complex pattern: Right-aligned triangle
print("\n8. Right-aligned triangle pattern:")
height = 5
for i in range(1, height + 1):
    for space in range(height - i):
        print(" ", end="")
    for star in range(i):
        print("*", end="")
    print()
