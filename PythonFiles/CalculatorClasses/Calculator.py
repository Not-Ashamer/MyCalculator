from Exceptions.BasicInvalidExpressionException import BasicInvalidExpressionException
from .Operator import Operator
from .OpType import OpType
from math import pow #AND NOTHING ELSE!!!!
from . import OperationMethods
from . import HelperMethods
from Exceptions.UnrecognizedCharacterException import UnrecognizedCharacterException

# TODO: here we import the functions we make manually like average or negation

class Calculator:
    def __init__(self):
        """
        Initializes the Calculator with a registry of supported operators.
        """
        # We store the operators in a dictionary for O(1) lookup.
        self.operators: dict = self._init_operators(self)

    def calculate(self, expression: str) -> float:
        """
        The big method that does all the work. (The boss)
        Receives a raw string, processes it, and returns the result.
        """
        # Step 0: Simplify the string to make tokenization simple
        expression = self._simplify_expression(expression)
        # Step 1: Tokenize (make a list of what matters from the string)
        tokens: list = self._tokenize(expression)

        # Step 2: Validate (using the operator's given values, check that they're valid
        if  not self._is_valid_expression(self,tokens):
            raise BasicInvalidExpressionException(f"The expression {expression} is not valid.")

        # Step 3: Parse (Shunting-Yard) & Evaluate
#TODO: THE ACTUAL CALCULATION DIPSHIT

        print(f"Debug Tokens: {tokens}")  # Temporary for testing
        return 0.6742069  # Placeholder (THE DAY THIS IS THE RESULT OF A CALCULATION I'M GONNA KILL MYSELF)

    def _tokenize(self, expression: str) -> list:
        """
        Scans the input string and converts it into a list of tokens.
        Example: "5 + 33" -> ["5", "+", "33"]
        """
        tokens = []
        i = 0
        length = len(expression)

        while i < length:
            char = expression[i]
            # sum numbers
            if char.isdigit() or char == '.'or self.is_unary_negative(expression, i, self.operators):
                number_str = char
                i += 1
                # grab characters as long as they are digits or dots
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    number_str += expression[i]
                    i += 1
                tokens.append(number_str)
                continue

            # Handle Operators and Parentheses
            #  assume single-character operators
            if char in self.operators or char in "()":
                tokens.append(char)
                i += 1
                continue



            # If unrecognized character we have an exception
            raise UnrecognizedCharacterException(f"The character {char} at index {i} is not recognized.")

        return tokens
    @staticmethod
    def _init_operators(self) -> dict:
        """
        Creates and returns the dictionary of supported operators.
        """
        mydict={
            "+": Operator("+", 1, lambda a, b: a + b, OpType.INFIX),
            "-": Operator("-", 1, lambda a, b: a - b, OpType.INFIX),
            "*": Operator("*", 2, lambda a, b: a * b, OpType.INFIX),
            "/": Operator("/", 2, lambda a, b: a / b, OpType.INFIX),
            "^": Operator("^", 3, lambda a, b: pow(a, b), OpType.INFIX),
            "!": Operator("!", 6, lambda a: OperationMethods.factorial(a), OpType.POSTFIX),
            "~": Operator("~", 6, lambda a: -a, OpType.PREFIX),
            "@": Operator("@", 5, lambda a, b: OperationMethods.average(a, b), OpType.INFIX),
            "&": Operator("&", 5, lambda a, b: OperationMethods.minimum(a, b), OpType.INFIX),
            "$": Operator("$", 5, lambda a, b: OperationMethods.maximum(a, b), OpType.INFIX),
            "%": Operator("%", 4, lambda a, b: a % b, OpType.INFIX),
            # Add more hereL
        }
        current_max_precedence = max(op.precedence for op in mydict.values())
        mydict["unary_minus"]= Operator("unary_minus",current_max_precedence+1, lambda a: -a, OpType.PREFIX)
        return mydict
    @staticmethod
    def _is_valid_expression(self, tokens: list) -> bool:
        if not HelperMethods.parentheses_balanced(tokens):
            raise BasicInvalidExpressionException(f"The expression {tokens} has unbalanced parentheses.")
        i=0
        while i < len(tokens):
            token = tokens[i]
            if HelperMethods.is_number(token):
                i+=1
                continue
            #if token in '()':
        return True

    def is_unary_negative(self, expression: str, index : int, operators : dict) -> bool:
        if(expression[index] != "-"):
            return False
        if(index>0):
            previndex = index-1
            if(expression[previndex] == ")"):
                return False
            if(str.isdigit(expression[previndex])):
                return False
            if(expression[previndex] in operators):
                return operators[expression[previndex]].op_type==OpType.POSTFIX
        return True
    def _simplify_expression(self, expression: str) -> str:
        """Returns a string without unecessary characters, which makes tokenization easier and will more clearly find problems"""
        expression = expression.replace(" ", "") #remove whitespace entirely
        expression = self._compress_minuses(expression)
        return expression
    def _compress_minuses(self, expression: str) -> str:
        """This program squishes repeated minus signs, where ----- is the same as -,
        and ------- is the same as -- because it's unknown yet whether either of the minuses are unary or binary"""
        compressed =[]
        i=0
        while i<len(expression):
            char = expression[i]
            if char == "-":
                count = 1
                i+=1
                while(i < len(expression)):
                    if not (expression[i]=="-"):
                        break
                    count += 1
                    i+=1
                compressed.append("-")
                if count%2==0:
                    compressed.append("-")
            else:
                compressed.append(char)
                i+=1
        return "".join(compressed)
