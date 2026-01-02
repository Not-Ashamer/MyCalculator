from PythonFiles import pythonConfig
from PythonFiles.CalculatorClasses.Calculator import Calculator


def accept_input() -> None:
    print(
        "Please enter a valid mathematical expression, or \"quit\" to exit, or \"rules\" for the rules of the calculator!")
    user_input = input("> ")
    if user_input == "quit":
        exit()
    if user_input == "rules":
        print(pythonConfig.CALCULATOR_RULES)
        accept_input()
        return
    calculate_method(user_input)


def calculate_method(user_input: str) -> None:
    my_calculator = Calculator()
    try:
        print(my_calculator.calculate(user_input))
    except ZeroDivisionError:
        print("ERROR: Division by zero")
    except OverflowError:
        print("ERROR: result is too large")
    except ValueError as e:
        print(f"ERROR: Math Error: {e}")
    except Exception as e:
        print(f"ERROR: Invalid Expression: {e}")
    finally:
        accept_input()


def main():
    print("Welcome to the Omega Calculator by Me!")
    accept_input()
    print("Bye Bye!")


if __name__ == '__main__':
    main()
