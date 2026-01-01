from PythonFiles.CalculatorClasses.Calculator import Calculator

def main():
    print("Please enter a mathematical Expression.")
    mycalc = Calculator()
    exp = "(2---~-3!)"
    print(mycalc.calculate(exp))
if __name__ == '__main__':
    main()