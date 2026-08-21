import time

# 1. Recursive Implementation
def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# 2. Iterative Implementation
def fibonacci_iterative(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Performance Comparison
n = 35

start = time.time()
rec_res = fibonacci_recursive(n)
rec_time = time.time() - start

start = time.time()
iter_res = fibonacci_iterative(n)
iter_time = time.time() - start

print(f"Fibonacci({n}) = {rec_res}")
print(f"Recursive Time: {rec_time:.6f} seconds")
print(f"Iterative Time: {iter_time:.6f} seconds")