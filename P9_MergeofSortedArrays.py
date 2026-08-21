print("_________________________________________________________")
n = int(input("***Enter size of first array (n): "))
arr1 = list(map(int, input(f"Enter {n} elements: ").split()))

m = int(input("***Enter size of second array (m): "))
arr2 = list(map(int, input(f"Enter {m} sorted elements: ").split()))

merged = arr1 + arr2

while True:
    swapped = False
    for j in range(0, n+m-1):
        if merged[j] > merged[j + 1]:
            tem = merged[j + 1]
            merged[j + 1] = merged[j]
            merged[j] = tem
            swapped = True
            
    if not swapped:
        break

print(f"Merged sorted array: {merged}")