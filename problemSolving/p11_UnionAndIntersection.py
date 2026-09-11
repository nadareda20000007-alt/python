print("_________________________________________________________")


n = int(input("Enter size of first array: "))
X_arr1 = input("Enter elements separated by spaces: ").split()
m = int(input("Enter size of second array: "))
X_arr2 = input("Enter elements separated by spaces: ").split()


arr1 = []
for i in X_arr1:
    num = int(i)
    if num not in arr1:
        arr1.append(num)


arr2 = []
for i in X_arr2:
    num = int(i)
    if num not in arr2:
        arr2.append(num)


intersection = []
for i in arr1:
    if i in arr2:
        intersection.append(i)


union = []
for i in arr1:
    union.append(i)
for i in arr2:
    if i not in union:
        union.append(i)


print("**Array1:", arr1)
print("**Array2:", arr2)
print("**Union:", union)
print("**Intersection:", intersection)
print("_________________________________________________________")