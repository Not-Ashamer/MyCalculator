from math import pow  # AND NOTHING ELSE!!!


def add(a: float, b: float) -> float:
    if a is None or b is None:
        raise ValueError(f"a is {a} and b is {b} in addition")
    return a + b


def subtract(a: float, b: float) -> float:
    if a is None or b is None:
        raise ValueError(f"a is {a} and b is {b} in subtraction")
    return a - b


def multiply(a: float, b: float) -> float:
    if a is None or b is None:
        raise ValueError(f"a is {a} and b is {b} in multiplication")
    return a * b


def divide(a: float, b: float) -> float:
    if a is None or b is None:
        raise ValueError(f"a is {a} and b is {b} in division")
    if b == 0:
        raise ZeroDivisionError(f"Division by zero")
    return a / b


def modulus(a: float, b: float) -> float:
    if a is None or b is None:
        raise ValueError(f"a is {a} and b is {b} in modulation")
    if b == 0:
        raise ZeroDivisionError(f"Division by zero")
    return a % b


def exponent(a: float, b: float) -> float:
    if a is None or b is None:
        raise ValueError(f"a is {a} and b is {b} in exponent")
    if a < 0 and (int(b) != b):
        raise ValueError(f"{a} is negative, cannot calculate root of negative number ")
    if a == 0 and b == 0:
        raise ValueError(f"0^0 is undefined")
    return pow(a, b)


def negation(a: float) -> float:
    if a is None:
        raise ValueError(f"a is {a} in negation")
    return -a


def factorial(a: float) -> float:
    if a is None:
        raise ValueError(f"a is {a} in factorial")
    if a < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if a != int(a):
        raise ValueError(f"Factorial of non integer number {a}")
    if a == 0 or a == 1:
        return 1
    a = int(a)
    factorial_sum = 1
    for i in range(2, a + 1):
        factorial_sum *= i
    return factorial_sum


def average(a: float, b: float) -> float:
    return (a + b) / 2


def minimum(a: float, b: float) -> float:
    return a if a < b else b


def maximum(a: float, b: float) -> float:
    return a if a > b else b


def negation_special_check(token: str):
    """The tilde can only be placed to the right of a number, no operators allower, which is"""
    return token == "(" or str.isdigit(token)


def sum_digits(a: float) -> float:
    """Sums the digits of a number repeatedly until it is single digit"""
    sign = -1 if a < 0 else 1
    a = a * sign
    while a != int(a):
        a *= 10
    sum_of_digits = 0
    while a > 0:
        sum_of_digits += a % 10
        a //= 10
    if sum_of_digits > 9:
        sum_of_digits = sum_digits(sum_of_digits)
    return sum_of_digits * sign
