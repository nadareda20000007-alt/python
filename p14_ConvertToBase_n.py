number = int(input("Enter a decimal number: "))
base = int(input("Enter the base to convert to : "))

if base < 1 or base > 36:
    print("Invalid base! Please enter a base between 1 and 36.")
elif number == 0:
    print("The number in base", base, "is:", "0" if base != 1 else " ")
elif base == 1:
    print("The number in base 1 is:", "1" * number)
else:
    answer = []
    num = number

    while num > 0:
        remainder = num % base
        
        if remainder < 10:
            answer.append(str(remainder))
        else:
            answer.append(chr(remainder - 10 + ord('A')))
            
        num = num // base

    answer.reverse()
    print("The number in base", base, "is:", "".join(answer))