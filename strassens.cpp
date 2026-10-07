// Run with:
// g++ -O3 strassens.cpp -o strassens
// ./strassens

/*
    Sources:
        1. https://www.geeksforgeeks.org/dsa/strassens-matrix-multiplication-algorithm-implementation/

        2. https://gemini.google.com/app
        - prompt: "Take a look at this implementation and determine if it can be optimized
                    -- I only need to test 256x256 use std:vector?"

    Why is Strassen's faster in C++?
    1. Compiled directly to machine code (no interpreter overhead)
    2. No Python style object boxing or reference counting lag
        - Object boxing: wrapping primitives (numbers in our case) inside a full memory object complete with extra type metadata and reference tracking overhead
        - Reference counting lag: is the CPU processing overhead caused by a runtime constantly tracking and updating object reference counts every time they are created, shared, or destroyed
    3. Low overhead memory handling during recursion and matrix slicing
        - Matrix slicing: Every time you split a matrix in half recursively, the program has to define where the sub-matrix starts, where it ends, and how its rows and columns map out.

*/

#include <iostream>
#include <vector>
#include <chrono>
#include <random>

using namespace std;

// Define a 2D matrix type for convenience
using Matrix = vector<vector<double>>;

// Helper function to build a random matrix
Matrix build_matrix(int n) {
    Matrix mat(n, vector<double>(n));
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<double> dis(0.0, 100.0);
    
    for(int i = 0; i < n; ++i) {
        for(int j = 0; j < n; ++j) {
            mat[i][j] = dis(gen);
        }
    }
    return mat;
}

// Matrix Addition
Matrix add(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, vector<double>(n));
    for(int i = 0; i < n; ++i)
        for(int j = 0; j < n; ++j)
            C[i][j] = A[i][j] + B[i][j];
    return C;
}

// Matrix Subtraction
Matrix sub(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, vector<double>(n));
    for(int i = 0; i < n; ++i)
        for(int j = 0; j < n; ++j)
            C[i][j] = A[i][j] - B[i][j];
    return C;
}

// Standard 3-loop method
Matrix standard_method(const Matrix& mat_a, const Matrix& mat_b) {
    int n = mat_a.size();
    Matrix result(n, vector<double>(n, 0.0));
    for(int i = 0; i < n; ++i) {
        for(int j = 0; j < n; ++j) {
            for(int k = 0; k < n; ++k) {
                result[i][j] += mat_a[i][k] * mat_b[k][j];
            }
        }
    }
    return result;
}

// Strassen's method with a hybrid base case threshold
Matrix strassens_method(const Matrix& mat_a, const Matrix& mat_b) {
    int n = mat_a.size();

    // Base Case / Hybrid Threshold: switch to standard loops for small blocks
    if (n <= 64) {
        return standard_method(mat_a, mat_b);
    }

    int mid = n / 2;
    Matrix A11(mid, vector<double>(mid)), A12(mid, vector<double>(mid)),
           A21(mid, vector<double>(mid)), A22(mid, vector<double>(mid));
    Matrix B11(mid, vector<double>(mid)), B12(mid, vector<double>(mid)),
           B21(mid, vector<double>(mid)), B22(mid, vector<double>(mid));

    // Divide into quadrants
    for(int i = 0; i < mid; ++i) {
        for(int j = 0; j < mid; ++j) {
            A11[i][j] = mat_a[i][j];
            A12[i][j] = mat_a[i][j + mid];
            A21[i][j] = mat_a[i + mid][j];
            A22[i][j] = mat_a[i + mid][j + mid];

            B11[i][j] = mat_b[i][j];
            B12[i][j] = mat_b[i][j + mid];
            B21[i][j] = mat_b[i + mid][j];
            B22[i][j] = mat_b[i + mid][j + mid];
        }
    }

    // Conquer (7 recursive calls)
    Matrix SM_1 = strassens_method(add(A11, A22), add(B11, B22));
    Matrix SM_2 = strassens_method(add(A21, A22), B11);
    Matrix SM_3 = strassens_method(A11, sub(B12, B22));
    Matrix SM_4 = strassens_method(A22, sub(B21, B11));
    Matrix SM_5 = strassens_method(add(A11, A12), B22);
    Matrix SM_6 = strassens_method(sub(A21, A11), add(B11, B12));
    Matrix SM_7 = strassens_method(sub(A12, A22), add(B21, B22));

    // Compute final quadrants
    Matrix C11 = add(sub(add(SM_1, SM_4), SM_5), SM_7);
    Matrix C12 = add(SM_3, SM_5);
    Matrix C21 = add(SM_2, SM_4);
    Matrix C22 = add(add(sub(SM_1, SM_2), SM_3), SM_6);

    // Combine quadrants back into one matrix
    Matrix C(n, vector<double>(n));
    for(int i = 0; i < mid; ++i) {
        for(int j = 0; j < mid; ++j) {
            C[i][j] = C11[i][j];
            C[i][j + mid] = C12[i][j];
            C[i + mid][j] = C21[i][j];
            C[i + mid][j + mid] = C22[i][j];
        }
    }
    return C;
}

int main() {
    int size = 256; // Try 256x256 or 512x512
    cout << "\nBuilding matrices of size " << size << "x" << size << "..." << endl;
    Matrix A = build_matrix(size);
    Matrix B = build_matrix(size);

    // Benchmark Standard Method
    auto start = chrono::high_resolution_clock::now();
    Matrix res_std = standard_method(A, B);
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed_std = end - start;
    cout << "Standard 3-Loop Method Time: " << elapsed_std.count() << " seconds." << endl;

    // Benchmark Strassen's Method
    start = chrono::high_resolution_clock::now();
    Matrix res_strassen = strassens_method(A, B);
    end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed_strassen = end - start;
    cout << "Strassen's Method Time:     " << elapsed_strassen.count() << " seconds." << endl;

    return 0;
}
