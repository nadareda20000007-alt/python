def sum_of_digits(n):
    n = abs(n)
    total = 0
    for digit in str(n):
        total += int(digit)
    return total

def main():
    number = int(input("Enter a number: "))
    result = sum_of_digits(number)
    print(f"The sum of the digits is: {result}")

if __name__ == "__main__":
    main()