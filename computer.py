import sys
import re
from Operation import Operation


def parse_expression(equation):
    equation = (
        equation.replace(" ", "")
        .replace("\t", "")
        .replace("\n", "")
        .replace("+", " +")
        .replace("-", " -")
        .replace("=", " = ")
    )
    equation = equation.split(" = ")
    for i in range(len(equation)):
        equation[i] = equation[i].strip()
    return equation


def reducer(operation):
    reg = re.search("([\+|-]?\d*\.?\d*)(\*)?(X|x)?(\^\d+\.?\d*)?", operation)
    if reg:
        reg = reg.groups()
    else:
        print("Input invalid")
        exit(0)

    # get first digit as coef if exist
    if reg[0]:
        try:
            coef = float(reg[0])
        except:
            coef = 1
    else:
        coef = 1

    if coef == 0:
        return 0, 0
    # get last digit as power if exist
    # power is equal to 0 if char "X" exist and 0 if not
    if reg[3]:
        power = reg[3].replace("^", "")
        if power.isdigit():
            try:
                power = float(power)
            except:
                power = 0
        else:
            print(f"Input error (power can't be a float number): {operation}")
            exit(0)
    elif reg[2] and reg[2].upper() == "X":
        power = 1
    else:
        power = 0

    return coef, power


def reduce_expression(equation_tab):
    minimized_dict = {}
    operation_array = []
    left_operation_tab = equation_tab[0].split(" ")
    right_operation_tab = equation_tab[1].split(" ")

    for operation in left_operation_tab:
        coef, power = reducer(operation)
        if power in minimized_dict:
            minimized_dict[power] += coef
        else:
            minimized_dict[power] = coef

    for operation in right_operation_tab:
        coef, power = reducer(operation)
        if power in minimized_dict:
            minimized_dict[power] -= coef
        else:
            minimized_dict[power] = -coef

    for power, coef in sorted(minimized_dict.items()):
        if coef != 0:
            operation_array.append(Operation(coef, power))

    # return sorted array of Operation objects
    return sorted(operation_array, key=lambda x: x.power)


def print_reduced_equation(operation_array):
    print("Reduced form: ", end="")

    if len(operation_array) == 0:
        print("0", end=" ")
    for index, operation in enumerate(operation_array):
        coef_str = str(operation.coef)
        if index != 0:
            if operation.coef >= 0:
                print("+ ", end="")
            else:
                coef_str = coef_str.replace("-", "")
                print("- ", end="")
        if operation.coef == 0:
            print("0", end=" ")
        else:
            print(f"{coef_str} * X^{operation.power}", end=" ")
    print("= 0\n")


def resolve_second_degre(operation_array):
    a = 0
    b = 0
    c = 0

    for operation in operation_array:
        if operation.power == 0:
            c = operation.coef
        elif operation.power == 1:
            b = operation.coef
        elif operation.power == 2:
            a = operation.coef

    print(f"a = {a}\nb = {b}\nc = {c}")

    discr = (b ** 2) - 4 * a * c
    print(f"Delta is equal to {discr}\n")

    if discr > 0:
        soluce_1 = (-b - (discr ** (1 / 2))) / (2 * a)
        soluce_2 = (-b + (discr ** (1 / 2))) / (2 * a)
        print(
            f"Discriminant is strictly positive, the two solutions are:\n{soluce_1}\n{soluce_2}"
        )
        return

    if discr == 0:
        soluce = -b / (2 * a)
        print(f"Discriminant is equal to zero, the solution is:\n{soluce}")

    if discr < 0:
        print(
            f"Discriminant is strictly negative, the solutions are:\n({-b} + i√{discr}) / {2 * a}\n({-b} - i√{discr}) / {2 * a}"
        )


def resolve_first_degre(operation_array):
    a = 0
    b = 0

    for operation in operation_array:
        if operation.power == 0:
            b = operation.coef
        elif operation.power == 1:
            a = operation.coef

    if b == 0:
        print("The solution is:\n0")
        exit(0)
    if a == 0:
        print("The solution is:\n0")
        exit(0)
    else:
        soluce = -b / a
        print(f"The solution is:\n{soluce}")


def compute(eq_str=None):
    if eq_str is not None:

        expression_tab = parse_expression(eq_str)

        if expression_tab[0] and expression_tab[1]:
            operation_array = reduce_expression(expression_tab)
            print_reduced_equation(operation_array)

            if len(operation_array) > 0:
                equation_degre = operation_array[-1].power
            else:
                equation_degre = 0
            print(f"Polynomial degree: {equation_degre:g}")

            if equation_degre > 2:
                print(
                    f"The polynomial degree is strictly greater than 2, I can't solve."
                )

            if equation_degre == 2:
                resolve_second_degre(operation_array)

            if equation_degre == 1:
                resolve_first_degre(operation_array)

            if equation_degre == 0:
                if operation_array:
                    print("There is no solution")
                    exit(0)
                else:
                    print("All the ℝ is a solution")
                    exit(0)

        else:
            print("Input invalid")
            exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        eq_str = sys.argv[1]
        arg_len = len(eq_str.split("="))

        if arg_len == 2:
            compute(eq_str)

        elif arg_len == 1:
            print(f"No '=' in the expression: '{eq_str}'")
            exit(0)

        else:
            print(f"Multiple '=' found in the expression: '{eq_str}'")
            exit(0)

    else:
        print("Wrong format:\n  Usage: Python3 <equation>")
