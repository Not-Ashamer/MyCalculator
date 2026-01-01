from PythonFiles.CalculatorClasses.Calculator import Calculator

# "+": Operator("+", 1, lambda a, b: a + b, OpType.INFIX),
# "-": Operator("-", 1, lambda a, b: a - b, OpType.INFIX),
# "*": Operator("*", 2, lambda a, b: a * b, OpType.INFIX),
# "/": Operator("/", 2, lambda a, b: a / b, OpType.INFIX),
# "^": Operator("^", 3, lambda a, b: pow(a, b), OpType.INFIX, associativity='R'),
# "!": Operator("!", 6, lambda a: OperationMethods.factorial(a), OpType.POSTFIX),
# "~": Operator("~", 6, lambda a: -a, OpType.PREFIX, associativity='R', accepted_right_types=[]),
# "@": Operator("@", 5, lambda a, b: OperationMethods.average(a, b), OpType.INFIX),
# "&": Operator("&", 5, lambda a, b: OperationMethods.minimum(a, b), OpType.INFIX),
# "$": Operator("$", 5, lambda a, b: OperationMethods.maximum(a, b), OpType.INFIX),
# "%": Operator("%", 4, lambda a, b: a % b, OpType.INFIX),
# "#": Operator("#", 6, lambda a: OperationMethods.sum_digits(a), OpType.POSTFIX),
# "unary_minus": Operator("unary_minus", 2.5, lambda a: -a, OpType.PREFIX, associativity='R')
def main():
    print("Please enter a mathematical Expression.")
    my_calc = Calculator()
    exp = "(1.1.1)"
    print(my_calc.calculate(exp))
if __name__ == '__main__':
    main()