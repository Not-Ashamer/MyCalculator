from math import pow #AND NOTHING ELSE!!!

def add(a:float,b:float)->float:
    if a is None or b is None:
        raise ValueError(f"ERROR: a is {a} and b is {b} in addition")
    return a+b
def subtract(a:float,b:float)->float:
    if a is None or b is None:
        raise ValueError(f"ERROR: a is {a} and b is {b} in subtraction")
    return a-b
def multiply(a:float,b:float)->float:
    if a is None or b is None:
        raise ValueError(f"ERROR: a is {a} and b is {b} in multiplication")
    return a*b
def divide(a:float,b:float)->float:
    if a is None or b is None:
        raise ValueError(f"ERROR: a is {a} and b is {b} in division")
    return a/b
def modulus(a:float,b:float)->float:
    if a is None or b is None:
        raise ValueError(f"ERROR: a is {a} and b is {b} in modulation")
    if b==0:
        raise ZeroDivisionError(f"ERROR: Division by zero")
    return a%b
def exponent(a:float,b:float)->float:
    if a is None or b is None:
        raise ValueError(f"a is {a} and b is {b} in exponent")
    return pow(a,b)
def negation(a:float)->float:
    if a is None:
        raise ValueError(f"a is {a} in negation")
    return -a
def factorial(n:float)->float:
    if n<0:
        raise ValueError("Factorial of negative number")
    if int(n)!=n:
        raise ValueError(f"Factorial of non integer number {n}")
    n=int(n)
    factorial_sum=1
    for i in range(2,n+1):
        factorial_sum*=i
    return factorial_sum
def average(a:float,b:float)->float:
    return (a+b)/2
def minimum(a:float,b:float)->float:
    return a if a<b else b
def maximum(a:float,b:float)->float:
    return a if a>b else b
def negation_special_check(token:str):
    """The tilde can only be placed to the right of a number, no operators allower, which is"""
    return token=="(" or str.isdigit(token)
def sum_digits(a:float) ->float:
    sign = -1 if a<0 else 1
    a = a*sign
    while a!=int(a):
        a*=10
    sum_of_digits=0
    while a>0:
        sum_of_digits+=a%10
        a//=10
    if sum_of_digits>10:
        sum_of_digits=sum_digits(sum_of_digits)
    return sum_of_digits*sign

