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
    matrix = np.random.rand(x, y)
    return matrix


def standard_method(matrix: list) -> None:
    """
    implement standard matrix multiplication approach
    using 3 loops
    """

    return


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

    mtx = build_matrix(1024, 1024)
    standard_method(mtx)
    strassens_method(mtx)


    ## benchmarking ##
    start_time = time.perf_counter()
    """
    function goes here
    """
    elapsed_time = time.perf_counter() - start_time
    print(f"Time taken: {elapsed_time}")

