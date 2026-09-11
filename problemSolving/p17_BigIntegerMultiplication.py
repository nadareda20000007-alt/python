def num(a):
    print("Enter the number: ")
    number = int(input())

    done = False
    while not done:
        if len(str(number)) == 0:
            print(f"enter number with {a} digits.")
            print("Enter the number: ")
            number = int(input())
        elif len(str(number)) != a:
            print(f"enter a number with exactly {a} digits.")
            print("Enter the number: ")
            number = int(input()) 
        else :
            done= True 
    return number

def multi(x, y):
    str_x = str(x)
    str_y = str(y)
    
    max_len = max(len(str_x), len(str_y))
    str_x = str_x.zfill(max_len)
    str_y = str_y.zfill(max_len)
    str_x = int(str_x)
    str_y = int(str_y)
    result = str_x * str_y
    return result

def main():
    print ("______Sample Input______: ")
    n = int(input("Enter the size of first number: "))
    num_1 = num (n)
    m = int(input("Enter the size of second number: "))
    num_2 = num (m)
    print ("                                       ")
    print ("______Sample Output______: ")
    print ("the answer = " + str(multi(num_1, num_2)))



if __name__ == "__main__":
    main()