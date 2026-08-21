
import math

n = int(input("Enter an integer (n <= 12): ").strip())

if 0 <= n <= 12:
    result = math.factorial(n)
    print(f"factorial {n} is = {result}")
else:
    print("Please enter a +ve int <= 12.")