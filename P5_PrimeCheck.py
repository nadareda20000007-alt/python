#Given an integer n, your program should test whether it is a prime number or not.
#A prime number is a whole number greater than \(1\), that can only be divided evenly by \(1\) and itself. This means it has exactly two distinct factors.


n = int(input("Enter an int to find if its prime number or not: ").strip())

if n <= 1:
    is_prime = False
else:
    is_prime = True
    for i in range(2, n-2):
        if n % i == 0:
            is_prime = False
            break

if is_prime:
    print(f"{n} is a prime number.")
else:
    print(f"{n} is not a prime number.")