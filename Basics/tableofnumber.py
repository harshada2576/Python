# Get input from the user
num = int(input("Enter a number to display its multiplication table: "))

# Print the multiplication table
print(f"\nMultiplication Table for {num}:\n")
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")
