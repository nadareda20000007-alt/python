# Integers that are shifted off the right end are added back to the array from the left. Input Format    •First line contains two integers n and k.    • Second line contains n integers   .i dont get whats k


n = int(input("Enter size of array: "))
k= int(input("Enter the shift number: ").strip())
arr = []

while True:
    num = int(input(f"Enter number the {len(arr) + 1}st : "))
    arr.append(num)
    if len(arr) == n:
        break


k = k % n  # Handles cases where k is larger than n
shifted= [0] * n
for i in range(n):
    x = (i + k) % n
    shifted[i] = arr[x]


print("___________________________")
print("The Array:    ", arr)
print("shifted Array:", shifted)
