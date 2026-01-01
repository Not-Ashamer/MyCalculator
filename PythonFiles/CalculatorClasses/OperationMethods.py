
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


