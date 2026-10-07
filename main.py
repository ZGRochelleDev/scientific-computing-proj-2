"""
Name: Team JZ
Scientific Computing: proj 2
Dr. J
10/05/2026
"""


import numpy as np
import time
from pathlib import Path
import matplotlib.pyplot as plt

## ToDo:
# generate large matrix of ints
# implement standard method
# implement strassen's method
# implement some method to determine point of intersection
# add benchmarking
# add visualization


def build_matrix(x, y) -> list:
    """
    construct a matrix x * y
    We just need a matrix large enough to demonstrate strassen surpassing the std mathod.
    Maybe test 1024x1024, 32x32, 128x128?
    Source: https://en.wikipedia.org/wiki/Strassen_algorithm#Algorithm
    """
    matrix = np.random.randint(0, 100, size=(x, y), dtype=np.int32)
    return matrix


def standard_method(mat_a, mat_b) -> None:
    """
    implement standard matrix multiplication approach
    using 3 loops
    """
    # Converting parameters to numpy arrays
    mat_a = np.array(mat_a)
    mat_b = np.array(mat_b)
    # Getting dimensions of each array
    rows_a, cols_a = mat_a.shape
    rows_b, cols_b = mat_b.shape
    # Check that the cols of A = rows of B
    assert cols_a == rows_b, "Columns of mat_a must match Rows of mat_b."
    # Initializing the result matrix with the correct dimensions
    result = np.zeros((cols_b, rows_a))
    # standard matrix multiplication using 3 loops
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += mat_a[i][k] * mat_b[k][j]
    return result


def strassens_method(matrix: list) -> None:
    """
    implement the D&Q + recursive method
    """

    return


def plot_data(mtx_1, mtx_2) -> None:
    plt.figure(Path(__file__).name, figsize=(12, 8))
    plt.subplot(121).plot(mtx_1)
    plt.subplot(122).plot(mtx_2)
    plt.show()


if __name__ == '__main__':

    print("\nStarting...")

    mtx_1 = build_matrix(1024, 1024)
    mtx_2 = build_matrix(1024, 1024)

    # Quick test using the identity matrix
    mtx_3 = [[1,0],[0,1]]
    mtx_4 = [[1,2],[3,4]]
    print(standard_method(mtx_3, mtx_4)) 
    strassens_method(mtx_1)


    ## benchmarking ##
    start_time = time.perf_counter()
    """
    function goes here
    """
    standard_method(mtx_1, mtx_2)
    elapsed_time = time.perf_counter() - start_time
    print(f"Time taken: {elapsed_time}")

