import math


def get_range(val: int) -> tuple:
    """"
    this function is used to handle negative and positive looping values
    """

    start = 1
    stop = val + 1

    if val < 0:
        start = val - 1
        stop = 0

    return start, stop


def compute_discriminant(a, b, c) -> int:
    """
    Can use the formula: D = b^2 -4ac,
    to determine if the quad can be factored
    """

    return b**2 -(4 * a * c)


## Strassen's Method
def factor_quadratic_strassen(J: int, K: int, L: int):
    """
    Find one or more factors of the quadratic equation, returns false if not found

    Assume J, K, and L are positive integers, and that the quadratic is of the form:
        Jx^2 + Kx + L

    Factor the quadratic function:
        (Jx^2 + Kx + L) --> (x + p)(x + q)

    Slide 34 lecture notes
    """


    quad_to_solve = "{0}x^2 {1}x {2}".format(J, K, L)
    print(f"\nGiven the quadratic: {quad_to_solve}\n")


    ## find the GCD
    GCD = math.gcd(J, K, L)
    print(f"GCD: {GCD}")


    ## handle quads like X^2 + 1
    if compute_discriminant(J, K, L) < 0:
        print("Quadratic can not be factored")
        return


    ## factor out the GCD
    J, K, L = J//GCD, K//GCD, L//GCD


    ## factor J
    start, stop = get_range(J)
    for a in range(start, stop):
        if J % a == 0:
            c = J//a

            ## factor L
            start, stop = get_range(L)
            for b in range(start, stop):
                if L % b == 0:
                    d = L//b

                    ## compare to K
                    # L = bd and J = ac 
                    if ((a + b) * (c + d) - L - J) == K:

                        sign_func = lambda d: "+" if d >= 0 else ""
                        print(f"factor found: ({a}x {sign_func(b)} {b})({c}x {sign_func(d)} {d})")

                        ## convert the factor back into the original quadratic to make sure it matches
                        quad_solution = f"{(a * c) * GCD}x^2 {((a * d) + (b * c)) * GCD}x {(b * d) * GCD}"
                        print(f"check: {'Pass' if quad_solution == quad_to_solve else 'Fail'}\n")
                        return 1
    return 0


def main() -> None:

    if not factor_quadratic_strassen(-115425, -3254121, -379020):
        print("No factors found\n")

    if not factor_quadratic_strassen(115425, 3254121, 379021):
        print("No factors found\n")

    if not factor_quadratic_strassen(2, 0, 2):
        print("No factors found\n")


if __name__ == "__main__":
    main()
