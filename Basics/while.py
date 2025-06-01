# 1. Basic while loop
print("1. Basic while loop:")
count = 0
while count < 5:
    print(f"Count is {count}")
    count += 1

# 2. Using break
print("\n2. Using break:")
n = 0
while True:
    print(n)
    if n == 3:
        print("Breaking the loop.")
        break
    n += 1

# 3. Using continue
print("\n3. Using continue:")
i = 0
while i < 5:
    i += 1
    if i == 3:
        print("Skipping 3")
        continue
    print(i)

# 4. Using else with while
print("\n4. Using else with while:")
x = 0
while x < 3:
    print(f"x = {x}")
    x += 1
else:
    print("Loop finished without break.")

# 5. Else skipped due to break
print("\n5. Else skipped due to break:")
y = 0
while y < 5:
    if y == 2:
        break
    print(f"y = {y}")
    y += 1
else:
    print("This won't print due to break")

# 6. Simulating a for-loop with while
print("\n6. Simulating for-loop with while:")
index = 0
items = ['a', 'b', 'c']
while index < len(items):
    print(items[index])
    index += 1

# 7. Nested while loops (Simple Pattern)
print("\n7. Nested while loops:")
i = 1
while i <= 3:
    j = 1
    while j <= 3:
        print(f"{i} * {j} = {i*j}")
        j += 1
    print("-----")
    i += 1

# 8. Infinite loop (with manual break)
print("\n8. Infinite loop (safe):")
counter = 0
while True:
    print("Looping...")
    counter += 1
    if counter == 3:
        print("Breaking after 3 loops")
        break

# 9. Loop with user input (simulated)
print("\n9. User input loop simulation:")
responses = ["yes", "yes", "no"]  # simulate input
i = 0
while i < len(responses):
    response = responses[i]
    print(f"User said: {response}")
    if response == "no":
        print("Stopping based on user input.")
        break
    i += 1
