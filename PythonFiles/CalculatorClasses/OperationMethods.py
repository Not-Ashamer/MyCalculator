
def factorial(n:int):
    if(n<0):
        raise ValueError("Factorial of negative number")
    sum=1
    for i in range(2,n+1):
        sum*=i
    return sum
def average(a:float,b:float):
    return (a+b)/2
def minimum(a:float,b:float):
    return a if a<b else b
def maximum(a:float,b:float):
    return a if a>b else b
def negation_special_check(token:str):
    """The tilde can only be placed to the right of a number, no operators allower, which is"""
    return token=="(" or str.isdigit(token)
