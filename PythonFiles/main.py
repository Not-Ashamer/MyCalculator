from PythonFiles.CalculatorClasses.Calculator import Calculator

def main():
    print("Please enter a mathematical Expression.")
    mycalc = Calculator()
    exp = "(2---~*-3!)"
    exp = mycalc._simplify_expression(exp)
    print(exp)
    exp=mycalc._tokenize(exp)
    print(exp)
    exp = mycalc._validate_expression(exp)
    print(exp)
if __name__ == '__main__':
    main()