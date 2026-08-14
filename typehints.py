from typing import List

def average(scores: List[int]) -> float:
    return sum(scores) / len(scores)

# Correct usage
print("Average 1:", average([10, 20, 30]))

# Incorrect usage (bug)
print("Average 2:", average(["a", "b", "c"]))   # ❌ Wrong types


