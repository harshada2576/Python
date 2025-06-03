import os
import json
import csv

# ---------------------
# 1. Basic File Writing
# ---------------------
with open("example.txt", "w") as f:
    f.write("Line 1: Hello, World!\n")
    f.write("Line 2: File I/O demo.\n")

# -------------------
# 2. Appending to File
# -------------------
with open("example.txt", "a") as f:
    f.write("Line 3: Appended line.\n")

# -------------------------
# 3. Reading Entire Content
# -------------------------
with open("example.txt", "r") as f:
    print("Reading entire file:\n", f.read())

# --------------------
# 4. Using r+ (read/write)
# --------------------
with open("example.txt", "r+") as f:
    print("\nUsing r+:")
    print("Before write:", f.read())
    f.seek(0)
    f.write("Modified with r+\n")
    f.seek(0)
    print("After write:", f.read())

# --------------------
# 5. Using w+ (write/read)
# --------------------
with open("wplus_example.txt", "w+") as f:
    print("\nUsing w+: (truncates file)")
    f.write("Written with w+\nAnother line\n")
    f.seek(0)
    print("After write:", f.read())

# --------------------
# 6. Using a+ (append/read)
# --------------------
with open("aplus_example.txt", "a+") as f:
    f.write("Appended with a+\n")
    f.seek(0)
    print("\nUsing a+:")
    print(f.read())

# ---------------------
# 7. File Object Properties
# ---------------------
with open("example.txt", "r") as f:
    print("\nFile Properties:")
    print("Name:", f.name)
    print("Mode:", f.mode)
    print("Closed?:", f.closed)
print("Closed after context?:", f.closed)

# --------------------
# 8. Binary File I/O
# --------------------
binary_data = bytes([100, 120, 3, 255])
with open("binaryfile.bin", "wb") as f:
    f.write(binary_data)

with open("binaryfile.bin", "rb") as f:
    print("\nBinary File Read:", f.read())

# --------------------
# 9. JSON File Handling
# --------------------
data_dict = {"name": "Alice", "age": 30, "skills": ["Python", "AI"]}
with open("data.json", "w") as f:
    json.dump(data_dict, f)

with open("data.json", "r") as f:
    print("\nJSON Loaded:", json.load(f))

# --------------------
# 10. CSV File Handling
# --------------------
csv_rows = [["Name", "Age"], ["Bob", 25], ["Carol", 27]]
with open("people.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)

with open("people.csv", "r") as f:
    print("\nCSV Content:")
    for row in csv.reader(f):
        print(row)

# --------------------
# 11. File Existence Check
# --------------------
if os.path.exists("example.txt"):
    print("\n'example.txt' exists.")

# --------------------
# 12. File Rename & Delete
# --------------------
os.rename("example.txt", "renamed_example.txt")
print("File renamed to 'renamed_example.txt'")
os.remove("renamed_example.txt")
print("File 'renamed_example.txt' deleted.")

# --------------------
# 13. Exception Handling
# --------------------
try:
    with open("nonexistent.txt", "r") as f:
        f.read()
except FileNotFoundError as e:
    print("\nHandled Exception:", e)
