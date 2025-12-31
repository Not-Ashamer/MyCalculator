from Exceptions.BasicInvalidExpressionException import BasicInvalidExpressionException
from .Operator import Operator
from .CalculatorEnums import OpType
from math import pow #AND NOTHING ELSE!!!!
from . import OperationMethods
from . import HelperMethods
from Exceptions.UnrecognizedCharacterException import UnrecognizedCharacterException


def _is_valid_atom(token: str) -> bool:
    """Returns True if the token is anNumber or parenthesis"""
    return HelperMethods.is_number(token) or token in "()"


def _init_operators() -> dict:
    """
    Creates and returns the dictionary of supported operators.
    """
    mydict={
        "+": Operator("+", 1, lambda a, b: a + b, OpType.INFIX),
        "-": Operator("-", 1, lambda a, b: a - b, OpType.INFIX),
        "*": Operator("*", 2, lambda a, b: a * b, OpType.INFIX),
        "/": Operator("/", 2, lambda a, b: a / b, OpType.INFIX),
        "^": Operator("^", 3, lambda a, b: pow(a, b), OpType.INFIX, associativity='R'),
        "!": Operator("!", 6, lambda a: OperationMethods.factorial(a), OpType.POSTFIX),
        "~": Operator("~", 6, lambda a: -a, OpType.PREFIX, associativity='R',accepted_right_types=[]),
        "@": Operator("@", 5, lambda a, b: OperationMethods.average(a, b), OpType.INFIX),
        "&": Operator("&", 5, lambda a, b: OperationMethods.minimum(a, b), OpType.INFIX),
        "$": Operator("$", 5, lambda a, b: OperationMethods.maximum(a, b), OpType.INFIX),
        "%": Operator("%", 4, lambda a, b: a % b, OpType.INFIX),
        "unary_minus": Operator("unary_minus",2.5, lambda a: -a, OpType.PREFIX, associativity='R')
        # Add more here
    }
    return mydict


class Calculator:
    def __init__(self):
        """
        Initializes the Calculator with a registry of supported operators.
        """
        # We store the operators in a dictionary for O(1) lookup.
        self.operators: dict = _init_operators()

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
        if  not self._validate_expression(tokens):
            raise BasicInvalidExpressionException(f"The expression {expression} is not valid.")

        # Step 3: Parse (Shunting-Yard) & Evaluate
#TODO: THE ACTUAL CALCULATION DIPSHIT

        print(f"Debug Tokens: {tokens}")  # Temporary for testing
        return 0.6742069  # Placeholder (THE DAY THIS IS THE RESULT OF A CALCULATION I WILL KILL MYSELF)

    def _tokenize(self, expression: str) -> list:
        """
        Scans the input string and converts it into a list of tokens.
        Handles complex minus logic (Signs vs Operators).
        """

        tokens = []
        i = 0
        length = len(expression)

        while i < length:
            char = expression[i]

            # 1. Handle Numbers (Digits or dots)
            if HelperMethods.is_digit(char) or char == '.':
                number_str, new_i = self._read_number(expression, i)
                tokens.append(number_str)
                i = new_i
                continue

            # 2. Handle Minuses
            if char == '-':
                # Check if this minus is a "Sign" (glued to the next number)
                if self._is_part_of_sign(tokens):
                    minus_count = 0
                    while i < length and expression[i] == '-':
                        minus_count += 1
                        i += 1

                    if i < length and (HelperMethods.is_digit(expression[i]) or expression[i] == '.'):
                        number_str, new_i = self._read_number(expression, i)

                        if minus_count % 2 != 0:
                            number_str = "-" + number_str

                        tokens.append(number_str)
                        i = new_i
                    else:
                        for _ in range(minus_count):
                            tokens.append("unary_minus")
                    continue

                else:
                    if not tokens or tokens[-1] == "(" or (
                            tokens[-1] in self.operators and self.operators[tokens[-1]].op_type != OpType.POSTFIX):
                        tokens.append("unary_minus")
                    else:
                        tokens.append("-")

                    i += 1
                    continue

            # 3. Handle Other Operators and Parentheses
            if char in self.operators or char in "()":
                tokens.append(char)
                i += 1
                continue

            # 4. Handle Unrecognized Characters
            raise UnrecognizedCharacterException(f"The character '{char}' at index {i} is not recognized.")

        return tokens

    def _read_number(self, expression: str, i: int) -> tuple:
        """Helper to consume a number from the expression."""
        start = i
        # simple check for digit or dot
        while i < len(expression) and (HelperMethods.is_digit(expression[i]) or expression[i] == '.'):
            i += 1
        return "".join(expression[start:i]), i
    def _validate_expression(self, tokens: list) -> bool:
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

            # 1: Two values cannot be adjacent (e.g., "5 5", "5 (", ") 5")
            if self._has_adjacent_value(tokens, i):
                return False

            # 2: Operators must have valid neighbors
            if token in self.operators:
                if not self._validate_operator_neighbors(tokens, i):
                    return False

            # 3: Unknown tokens (Not an operator, number, or parenthesis)
            elif not _is_valid_atom(token):
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
        self.operators[token].check_neighbors(left, right, self.operators)
        return True
    def _is_unary_negative(self, expression: list, index : int) -> bool:
        """Determines if the given minus operator is binary or unary"""
        if index<0 or type(expression[index])!=str:
            return False
        if expression[index] != "-":
            return False
        if index>0:
            previndex = index - 1
            if expression[previndex] == ")":
                return False
            if str.isdigit(expression[previndex]):
                return False
            if expression[previndex] in self.operators:
                return self.operators[expression[previndex]].op_type != OpType.POSTFIX

        return True

    def _is_part_of_sign(self, tokens: list) -> bool:
        """
        Returns True if a minus at the current position should be treated as part of a number (Sign).
        Rule: True if Preceding token is an Infix or Prefix Operator.
        Rule: False if Preceding token is Number, ')', Postfix, or if we are at Start.
        """
        if not tokens:
            return False  # Start of line -> Unary Operator (Not Sign)

        prev = tokens[-1]

        if prev == "(":
            return False  # (-5) -> ( unary 5 ). Safer for precedence.

        if HelperMethods.is_number(prev) or prev == ")":
            return False  # 5 - 5 -> Binary Minus

        if prev in self.operators:
            op_type = self.operators[prev].op_type
            if op_type == OpType.POSTFIX:
                return False  # 5! - 5 -> Binary Minus

            return True  # 5 * -5 or ~ -5 -> Sign

        return False

    def _simplify_expression(self, expression: str) -> str:
        """Returns a string without unnecessary characters, which makes tokenization easier and will more clearly find problems"""
        expression = expression.replace(" ", "") #remove whitespace entirely
        return expression



