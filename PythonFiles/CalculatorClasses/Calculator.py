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
        self.operators: dict = self._init_operators()

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
        if  not self._is_valid_expression(tokens):
            raise BasicInvalidExpressionException(f"The expression {expression} is not valid.")

        # Step 3: Parse (Shunting-Yard) & Evaluate
#TODO: THE ACTUAL CALCULATION DIPSHIT

        print(f"Debug Tokens: {tokens}")  # Temporary for testing
        return 0.6742069  # Placeholder (THE DAY THIS IS THE RESULT OF A CALCULATION I WILL KILL MYSELF)

    def _tokenize(self, expression: str) -> list:
        """
        Scans the input string and converts it into a list of tokens.
        Example: "5 + 33" -> ["5", "+", "33"]
        """
        expression = self._convert_unary_minus(list(expression))
        tokens = []
        i = 0
        length = len(expression)

        while i < length:
            token = expression[i]
            # sum numbers
            if token.isdigit() or token == '.' or self._is_part_of_sign(expression, i):
                minus_count = 0
                if self._is_part_of_sign(expression, i):
                    minus_count += 1  # Count the first minus
                i += 1
                #count all the minuses instead of adding them in
                while i < length and self._is_part_of_sign(expression, i):
                    minus_count += 1
                    i += 1

                #get digit part of the number
                digit_part = ""
                #handle the case where the first char acquired was actually a digit and not a minus
                if token.isdigit() or token == '.':
                    digit_part = token
                #build digit
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    digit_part += expression[i]
                    i += 1

                #if minus_count is odd (1, 3, 5...), we prepend a single "-" else nothing
                final_number_str = digit_part
                if minus_count % 2 != 0:
                    final_number_str = "-" + digit_part
                tokens.append(final_number_str)
                continue

            #handle Operators and Parentheses
            #assume single-character operators
            if token in self.operators or token in "()":
                tokens.append(token)
                i += 1
                continue



            #if unrecognized character we have an exception
            raise UnrecognizedCharacterException(f"The character {token} at index {i} is not recognized.")
        return tokens
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
            "unary_minus": Operator("unary_minus",1, lambda a: -a, OpType.PREFIX)
            # Add more here
        }
        return mydict

    def _is_valid_expression(self, tokens: list) -> bool:
        """
        Returns True if the expression is syntactically valid, False otherwise.
        """
        # 1. Check for Empty Input
        if len(tokens)==0:
            return False

        # 2. Check Parentheses Balance
        if not HelperMethods.parentheses_balanced(tokens):
            # You might want to raise a specific exception here instead
            return False

        # 3. Check Sequence Rules (Adjacent values, Operator neighbors, etc.)
        if not self._validate_token_sequence(tokens):
            return False

        return True

    def _validate_token_sequence(self, tokens: list) -> bool:
        """Iterates through tokens to ensure no structural rules are broken."""
        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Rule A: Two values cannot be adjacent (e.g., "5 5", "5 (", ") 5")
            if self._has_adjacent_value(tokens, i):
                return False

            # Rule B: Operators must have valid neighbors
            if token in self.operators:
                if not self._validate_operator_neighbors(tokens, i):
                    return False

            # Rule C: Unknown tokens (Not an operator, number, or parenthesis)
            elif not self._is_valid_atom(token):
                return False

            i += 1
        return True

    def _has_adjacent_value(self, tokens: list, i: int) -> bool:
        """
        Checks if the current token and the next token are both 'Values'.
        Example of invalid: "5 5", "5 (", ") 5", "5! 5"
        """
        if i + 1 >= len(tokens):
            return False  # No next token, so no conflict possible

        current_token = tokens[i]
        next_token = tokens[i + 1]

        current_is_value = (HelperMethods.is_number(current_token) or
                            current_token == ")" or
                            Operator.is_postfix(current_token,self.operators))
        next_is_value = (HelperMethods.is_number(next_token) or
                         next_token == "(")

        return current_is_value and next_is_value

    def _validate_operator_neighbors(self, tokens: list, i: int) -> bool:
        """Delegates validation to the specific Operator instance."""
        token = tokens[i]
        left = tokens[i - 1] if i > 0 else None
        right = tokens[i + 1] if i + 1 < len(tokens) else None

        try:
            self.operators[token].check_neighbors(left, right, self.operators)
            return True
        except Exception:
            return False

    def _is_valid_atom(self, token: str) -> bool:
        """Returns True if the token is anNumber or parenthesis"""
        return HelperMethods.is_number(token) or token in "()"

    def _is_unary_negative(self, expression: list, index : int) -> bool:
        """Determines if the given minus operator is binary or unary"""
        if(index<0 or type(expression[index])!=str):
            return False
        if expression[index] != "-":
            return False
        if(index>0):
            previndex = index - 1
            if expression[previndex] == ")":
                return False
            if str.isdigit(expression[previndex]):
                return False
            if expression[previndex] in self.operators:
                return self.operators[expression[previndex]].op_type != OpType.POSTFIX

        return True
    def _is_part_of_sign(self,expression: list, index : int) -> bool:
        """Determines if the given minus is part of the sign rather than an operator.
            A minus is only explicitly part of the sign if it is to the right of a prefix operator"""
        if expression[index] != "unary_minus":
            return False
        if index>0:
            previndex = index-1
            if expression[previndex]in self.operators:
                return self.operators[expression[previndex]].op_type==OpType.PREFIX
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
    def _convert_unary_minus(self, tokens : list) -> list:
        i=0
        for i in range(len(tokens)):
            if(self._is_unary_negative(tokens,i)):
                tokens[i] = "unary_minus"
        return tokens


