x = 0
apples = int(input("Enter the number of apples: ").strip())

while apples % 12 != 0:
    apples = apples - 1
    x = x + 1

dozens = apples // 12

print(str(dozens) + " dozens and " + str(x) + " apples")





