# scientific-computing-proj-2

Team: JZ

Topic: Strassen's Method vs. Naive Multiplication

Our team will write a Python script to compare the standard nested loop matrix multiplication against Strassen's algebraic method.

The standard method is considered inefficient due to its use of 3 for-loops. Time Complexity O(n^3)

Strassen's method uses a recursive D&Q technique. Time Complexity O(n^log7) appx. O(n^2.81).

Source: https://en.wikipedia.org/wiki/Strassen_algorithm

We will add benchmarking and visualizations to demonstrate when Strassen's method overtakes the standard approach using large datasets.
