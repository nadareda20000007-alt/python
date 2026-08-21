import math

A = float(input("enter a: ").strip())
B = float(input("enter b: ").strip())
C = float(input("enter c: ").strip())
D = float(input("enter d: ").strip())
E = float(input("enter e: ").strip())  
F = float(input("enter f: ").strip())
G = float(input("enter g: ").strip())
X = float(input("enter x: ").strip())
Y = float(input("enter y: ").strip())

p1 = ((B // C) + A) // (D + (E // (F + G)))
p2 = math.sin(math.sqrt(X+ Y))

print(f"(c)- {p1}")
print(f"(d)- {p2}")