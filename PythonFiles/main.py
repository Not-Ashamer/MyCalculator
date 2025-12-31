from PythonFiles.CalculatorClasses.Calculator import Calculator

def main():
    print("Please enter a mathematical Expression.")
    mycalc = Calculator()
    exp = "5 - - - - 2 + -456 & 2"
    print(mycalc._tokenize(mycalc._simplify_expression(exp)))
if __name__ == '__main__':
    main()