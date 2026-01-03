import sys
import tkinter as tk
from tkinter import scrolledtext

from PythonFiles import pythonConfig
from PythonFiles.CalculatorClasses.Calculator import Calculator
from PythonFiles.Exceptions.BasicInvalidExpressionException import BasicInvalidExpressionException
from PythonFiles.Exceptions.InvalidOperatorUsageException import InvalidOperatorUsageException
from PythonFiles.Exceptions.InvalidParenthesisException import InvalidParenthesisException
from PythonFiles.Exceptions.UnrecognizedCharacterException import UnrecognizedCharacterException


class ConsoleRedirector:
    """A helper class that redirects print() statements to a Tkinter text widget."""

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.configure(state='normal')
        self.text_widget.insert('end', string)
        self.text_widget.see('end')
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass


class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Omega Calculator Console (GUI!!!)")
        self.root.geometry("600x400")

        self.calculator = Calculator()

        # 1. console screen
        self.console_output = scrolledtext.ScrolledText(root, state='disabled', height=15, bg="#000000", fg="#FFFFFF",
                                                        font=("Consolas", 10),width=28)
        self.console_output.pack(fill='both', expand=True, padx=5, pady=5)

        # 2. input
        self.input_field = tk.Entry(root, font=("Consolas", 12), bg="#222222", fg="white", insertbackground="white")
        self.input_field.pack(fill='x', padx=5, pady=(0, 5))
        self.input_field.focus_set()

        # 3. enter will end text reading
        self.input_field.bind('<Return>', self.process_input)

        sys.stdout = ConsoleRedirector(self.console_output)

        print("Welcome to my calculator!!!")
        print("Type 'rules' for rules or enter an expression. (or quit to leave)")
        print("-" * 40)

    def process_input(self, event=None):
        # get text and clear field
        expression = self.input_field.get()
        self.input_field.delete(0, 'end')

        if not expression.strip():
            return

        print(f">>> {expression}")  # Echo the user's input

        if expression.lower() == "quit":
            self.root.quit()
            return
        if expression.lower() == "rules":
            print(pythonConfig.CALCULATOR_RULES)
            return
        try:
            result = self.calculator.calculate(expression)
            print(f"Result: {result}")
        except (BasicInvalidExpressionException,
                InvalidOperatorUsageException,
                InvalidParenthesisException,
                UnrecognizedCharacterException) as e:
            print(f"Syntax Error: {e}")

        except ZeroDivisionError:
            print("Math Error: Division by Zero is not allowed.")
        except OverflowError:
            print("Math Error: Number too large.")
        except ValueError as e:
            print(f"Value Error: {e}")

        except Exception as e:
            print(f"Unexpected Error: {e}")

        print("-" * 40)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
