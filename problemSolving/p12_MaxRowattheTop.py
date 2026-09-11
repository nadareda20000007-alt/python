rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

matrix = []

for i in range(rows):
    row = []
    for j in range(cols):
        val = int(input(f"Enter value for row {i}, column {j}: "))
        row.append(val)
    matrix.append(row)


print("\nYour Matrix:")
for row in matrix:
    print(row)

sum_rows = [sum(row) for row in matrix]

for i in range(0 ,len(sum_rows)-1):
    for j in range(0, len(sum_rows)-1-i):
        if sum_rows[j] < sum_rows[j+1]:
            tem = sum_rows[j]
            sum_rows[j] = sum_rows[j+1]
            sum_rows[j+1] = tem

            tem = matrix[j]
            matrix[j] = matrix[j+1]
            matrix[j+1] = tem

        else:
            continue
    


print("\nYour arranged Matrix:")
for row in matrix:
    print(row)