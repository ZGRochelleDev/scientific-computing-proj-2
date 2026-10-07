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
    Maybe test 1024x1024, 32x32, 128x128?
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

    ## 2. Conquer - 7 recursive calls using native matrices math
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


# def plot_data(mtx_1, mtx_2) -> None:
#     plt.figure(Path(__file__).name, figsize=(12, 8))
#     plt.subplot(121).plot(mtx_1)
#     plt.subplot(122).plot(mtx_2)
#     plt.show()    print(type(mtx_1))


if __name__ == '__main__':

    print("\nStarting...")

    mtx_1 = build_matrix(128, 128)
    mtx_2 = build_matrix(128, 128)

    # Quick test using the identity matrix
    mtx_3 = [[1,0],[0,1]]
    mtx_4 = [[1,2],[3,4]]
    print(standard_method(mtx_3, mtx_4))
    print(strassens_method(mtx_3, mtx_4))

    ## benchmarking - Standard ##
    start_time = time.perf_counter()
    standard_method(mtx_1, mtx_2)
    elapsed_time = time.perf_counter() - start_time
    print(f"Time taken: {elapsed_time} seconds")

    ## benchmarking - Strassen's ##
    start_time = time.perf_counter()
    strassens_method(mtx_1, mtx_2)
    elapsed_time = time.perf_counter() - start_time
    print(f"Time taken: {elapsed_time} seconds")

