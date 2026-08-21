from os import name


def input_matrix(rows, cols):
    print(f"\n--- Enter elements for Matrix ({rows}x{cols}) ---")
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            val = int(input(f"Matrix [{i}][{j}]: "))
            row.append(val)
        matrix.append(row)
    return matrix


def print_matrix(matrix, name):
    print(f"\n{name}:")
    for row in matrix:
        print("  " + " ".join(f"{val:4d}" for val in row))


def multiply(matrix_A, matrix_B):
    rows_A = len(matrix_A)
    cols_A = len(matrix_A[0])
    rows_B = len(matrix_B)
    cols_B = len(matrix_B[0])

    if cols_A != rows_B:
        raise ValueError("Matrix dimensions are not compatible for multiplication.")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            total = 0
            for k in range(cols_A):
                total += matrix_A[i][k] * matrix_B[k][j]
            result[i][j] = total

    return result


def main():
    print("=== Matrix Multiplication (N x M) * (M x L) ===")

    N = int(input("Enter rows of Matrix A: "))
    M = int(input("Enter cols of Matrix A /rows of Matrix B: "))
    L = int(input("Enter cols of Matrix B: "))

    matrix_A = input_matrix(N, M)
    matrix_B = input_matrix(M, L)

    result = multiply(matrix_A, matrix_B)

    print_matrix(matrix_A, "Matrix A")
    print_matrix(matrix_B, "Matrix B")
    print_matrix(result, "Result Matrix (A x B)")



if __name__ == "__main__":
    main()