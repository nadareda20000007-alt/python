#The sine of x can be calculated approximately ,by summing the first N terms of the infinite series:
#sin(x) = x - x^3/3! + x^5/5! - x^7/7! + ... (x in radians)
#Write a program that reads in a value for x (in degrees) and then calculates its sine by summing the
#first N terms, where N represents a positive integer that is read along with the value of x.

import math

deg = float(input("Enter number in degrees: ").strip())
N = int(input("Enter N of terms: ").strip())

rad = math.radians(deg)
sin= 0.0

for i in range(N):
    power = 2 * i + 1
    term = ((-1) ** i) * (rad ** power) / math.factorial(power)
    sin = sin + term


print(f"\nApproximatly sin({deg}°)= {sin}")
