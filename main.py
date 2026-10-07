"""
Name: Team JZ
Scientific Computing: proj 2
Dr. J - Quinnipiac U
10/05/2026
"""


import numpy as np
import time
from pathlib import Path
import matplotlib.pyplot as plt
import sys

## ToDo:
# generate large matrix of ints
# implement standard method
# implement strassen's method
# implement some method to determine point of intersection
# add benchmarking
# add visualization


def build_matrix(x, y) -> np.ndarray:
    """
    construct a matrix x * y
    We just need a matrix large enough to demonstrate strassen surpassing the std mathod.
    Maybe test 32x32, 128x128, 1024x1024?
    Source: https://en.wikipedia.org/wiki/Strassen_algorithm#Algorithm
    """

    matrix = np.random.randint(0, 100, size=(x, y), dtype=np.int32)
    return matrix


def standard_method(mat_a, mat_b) -> np.ndarray:
    """
    implement standard matrix multiplication approach using 3 loops
    """
    # Converting parameters to numpy arrays
    mat_a = np.array(mat_a)
    mat_b = np.array(mat_b)
    # Getting dimensions of each array
    rows_a, cols_a = mat_a.shape
    rows_b, cols_b = mat_b.shape
    # Check that the cols of A = rows of B
    if cols_a != rows_b:
        raise ValueError("Columns of mat_a must match Rows of mat_b.")
    # Initializing the result matrix with the correct dimensions
    result = np.zeros((rows_a, cols_b))
    # standard matrix multiplication using 3 loops
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += mat_a[i][k] * mat_b[k][j]
    return result


## Our Strassen's implementation is slow due to:
#    1. the cost of recursion
#    2. the cost of managing the recursion tree
#    3. temporary submatrix allocations at every single step
def strassens_method(mat_a: np.ndarray, mat_b: np.ndarray) -> np.ndarray:
    """
    implement Strassen's method
    sources:
        https://www.geeksforgeeks.org/dsa/strassen-algorithm-in-python/
        https://medium.com/@devillar/the-strassens-algorithm-with-a-python-example-816002c2f7e6
        https://youtu.be/OSelhO6Qnlc?si=0IHA56hnVgl1AYP4
    """

    mat_a = np.asarray(mat_a)
    mat_b = np.asarray(mat_b)
    n = mat_a.shape[0]

    ## Base Case, a 1x1 matrix
    if n == 1:
        return mat_a * mat_b

    ## 1. Divide using NumPy's 2D matrix slicing
    # Assume power of 2, this will break on 3x3, etc.
    mid = n // 2
    A_11, A_12 = mat_a[:mid, :mid], mat_a[:mid, mid:]
    A_21, A_22 = mat_a[mid:, :mid], mat_a[mid:, mid:]
    
    B_11, B_12 = mat_b[:mid, :mid], mat_b[:mid, mid:]
    B_21, B_22 = mat_b[mid:, :mid], mat_b[mid:, mid:]

    ## 2. Conquer - 7 recursive calls using native matrix math
    SM_1 = strassens_method(A_11 + A_22, B_11 + B_22)
    SM_2 = strassens_method(A_21 + A_22, B_11)
    SM_3 = strassens_method(A_11, B_12 - B_22)
    SM_4 = strassens_method(A_22, B_21 - B_11)
    SM_5 = strassens_method(A_11 + A_12, B_22)
    SM_6 = strassens_method(A_21 - A_11, B_11 + B_12)
    SM_7 = strassens_method(A_12 - A_22, B_21 + B_22)

    ## 3. Compute final quadrants
    # Strassen's unique implementation is in this section
    C_11 = SM_1 + SM_4 - SM_5 + SM_7
    C_12 = SM_3 + SM_5
    C_21 = SM_2 + SM_4
    C_22 = SM_1 - SM_2 + SM_3 + SM_6

    ## 4. Combine quadrants into a single matrix using 
    # NumPy's block stitching to reconstruct the subproblem results.
    return np.block([[C_11, C_12], [C_21, C_22]])


def plot_data(matrix_sizes: list, standard_times: list, strassen_times: list) -> None:
    """
    plot the execution times
    """

    plt.figure(figsize=(10, 6))
    plt.plot(matrix_sizes, standard_times, marker='o', linestyle='-', linewidth=2, label='Standard 3-Loop Method')
    plt.plot(matrix_sizes, strassen_times, marker='s', linestyle='--', linewidth=2, label="Strassen's Method")
    
    plt.xlabel('Matrix Size (N x N)', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Performance Comparison: Standard vs. Strassen Matrix Multiplication', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.show()


def run_benchmarks(matrix_sizes: list) -> tuple:
    """
    Runs execution time benchmarks for both the standard method 
    and Strassen's method across a given list of matrix sizes.
    """

    standard_times = []
    strassen_times = []

    for size in matrix_sizes:
        print(f"Testing matrix size: {size}x{size}...")
        mtx_1 = build_matrix(size, size)
        mtx_2 = build_matrix(size, size)

        ## Standard Method
        start_time = time.perf_counter()
        standard_method(mtx_1, mtx_2)
        duration = time.perf_counter() - start_time
        standard_times.append(duration)
        print(f" - Standard: {duration} seconds")

        ## Strassen's Method
        start_time = time.perf_counter()
        strassens_method(mtx_1, mtx_2)
        duration = time.perf_counter() - start_time
        strassen_times.append(duration)
        print(f" - Strassen: {duration} seconds")

    return standard_times, strassen_times


if __name__ == '__main__':
    print("\nStarting...\n")

    matrix_sizes = [16, 32, 64, 128]
    
    # benchmarking loop
    standard_times, strassen_times = run_benchmarks(matrix_sizes)

    print("\nComplete")
    
    # Plot the 'execution time' by 'matrix size'
    plot_data(matrix_sizes, standard_times, strassen_times)
