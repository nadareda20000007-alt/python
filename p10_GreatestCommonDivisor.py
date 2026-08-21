a = int(input("Enter (a) (0 ≤ a < 1000): "))
b = int(input("Enter (b) (0 ≤ b < 1000): "))

if a>b:
    x=a
else:
    x=b

for i in range(1,x+1):
    if a%i==0 and b%i==0:
        gcd=i

print(f"GCD of {a} and {b} is: {gcd}")