
n, m = map(int, input("Enter dimensions n and m: ").split())

print(f"Enter the matrix ({n} rows, {m} elements per row):")
matrix = []
for i in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)

transposed = [[0] * n for _ in range(m)]

for i in range(n):
    for j in range(m):
        transposed[j][i] = matrix[i][j]

print("\nTransposed Matrix:")
for row in transposed:
    print(*row)



