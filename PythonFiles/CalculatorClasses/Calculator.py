from PythonFiles.Exceptions import InvalidParenthesisException
from PythonFiles.Exceptions.BasicInvalidExpressionException import BasicInvalidExpressionException
from PythonFiles.Exceptions.UnrecognizedCharacterException import UnrecognizedCharacterException
from . import HelperMethods
from . import OperationMethods
from .CalculatorEnums import OpType
from .Operator import Operator


def _is_valid_operand(token: str) -> bool:
    """Returns True if the token is a Number or parenthesis"""
    return HelperMethods.is_number(token) or token in "()"


def _init_operators() -> dict:
    """
    Creates and returns the dictionary of supported operators.
    """
    my_dict = {
        "+": Operator("+", 1, lambda a, b: OperationMethods.add(a, b), OpType.INFIX),
        "-": Operator("-", 1, lambda a, b: OperationMethods.subtract(a, b), OpType.INFIX),
        "*": Operator("*", 2, lambda a, b: OperationMethods.multiply(a, b), OpType.INFIX),
        "/": Operator("/", 2, lambda a, b: OperationMethods.divide(a, b), OpType.INFIX),
        "^": Operator("^", 3, lambda a, b: OperationMethods.exponent(a, b), OpType.INFIX, associativity='R'),
        "!": Operator("!", 6, lambda a: OperationMethods.factorial(a), OpType.POSTFIX),
        "~": Operator("~", 6, lambda a: OperationMethods.negation(a), OpType.PREFIX, associativity='R',
                      accepted_right_types=[]),
        "@": Operator("@", 5, lambda a, b: OperationMethods.average(a, b), OpType.INFIX),
        "&": Operator("&", 5, lambda a, b: OperationMethods.minimum(a, b), OpType.INFIX),
        "$": Operator("$", 5, lambda a, b: OperationMethods.maximum(a, b), OpType.INFIX),
        "%": Operator("%", 4, lambda a, b: OperationMethods.modulus(a, b), OpType.INFIX),
        "#": Operator("#", 6, lambda a: OperationMethods.sum_digits(a), OpType.POSTFIX),
        "unary_minus": Operator("unary_minus", 2.5, lambda a: OperationMethods.negation(a), OpType.PREFIX,
                                associativity='R')
        # Add more here
    }
    return my_dict


def _read_number(expression: str, i: int) -> tuple:
    """Helper to consume a number from the expression."""
    start = i
    dot_count = 0
    # simple check for digit or dot
    while i < len(expression) and (HelperMethods.is_digit(expression[i]) or expression[i] == '.'):
        if expression[i] == '.':
            if dot_count != 0:
                break
            dot_count += 1
        i += 1
    return "".join(expression[start:i]), i


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
        # Step 1: Tokenize (make a list of what matters from the string)
        tokens = self._tokenize(expression)

        # Step 2: Validate (using the operator's given values, check that they're valid
        self._validate_expression(tokens)
        # print("Before shunting yard: "+str(tokens))
        # Step 3: Parse (Shunting-Yard) & Evaluate
        tokens = self._shunting_yard(tokens)
        # print(f"Debug Tokens: {tokens}") # Temporary for testing
        return self._evaluate_postfix(tokens)

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
            # 0. Handle Whitespace
            if char == " ":
                i += 1
                continue
            # 1. Handle Numbers (Digits or dots)
            if HelperMethods.is_digit(char) or char == '.':
                number_str, new_i = _read_number(expression, i)
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
                        number_str, new_i = _read_number(expression, i)

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

    def _validate_expression(self, tokens: list) -> bool:
        """
        Returns True if the expression is syntactically valid, False otherwise.
        """
        # 1. Check for Empty Input
        if len(tokens) == 0:
            return False

        # 2. Check Parentheses Balance
        if not HelperMethods.parentheses_balanced(tokens):
            raise InvalidParenthesisException("The parentheses are not balanced")

        # 3. Check Sequence Rules (Adjacent values, Operator neighbors, etc.)
        if not self._validate_token_sequence(tokens):
            raise BasicInvalidExpressionException("The expression structure is invalid.")

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
            elif not _is_valid_operand(token):
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
                            Operator.is_postfix(current_token, self.operators))
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

    def _is_unary_negative(self, expression: list, index: int) -> bool:
        """Determines if the given minus operator is binary or unary"""
        if index < 0 or type(expression[index]) != str:
            return False
        if expression[index] != "-":
            return False
        if index > 0:
            prev_index = index - 1
            if expression[prev_index] == ")":
                return False
            if str.isdigit(expression[prev_index]):
                return False
            if expression[prev_index] in self.operators:
                return self.operators[expression[prev_index]].op_type != OpType.POSTFIX

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

    def _shunting_yard(self, tokens: list) -> list:
        """Receives a regular mathematical expression containing infix, prefix,and postfix operators,
           and converts it into postfix notation."""
        stack = []
        queue = []
        for item in tokens:
            if HelperMethods.is_number(item):
                queue.append(item)
                continue
            if item == "(":
                stack.append(item)
                continue
            if item in self.operators:
                while stack and stack[-1] in self.operators:
                    top = self.operators[stack[-1]]
                    curr = self.operators[item]
                    if top.precedence > curr.precedence or (
                            top.precedence == curr.precedence and curr.associativity == 'L'):
                        queue.append(stack.pop())
                    else:
                        break
                stack.append(item)
                continue
            if item == ")":
                while stack[-1] != "(":
                    queue.append(stack.pop())
                if not stack:
                    raise BasicInvalidExpressionException(f"Attempted pop from an empty stack!")
                stack.pop()
                continue
            raise UnrecognizedCharacterException("Unrecognized character in expression.")
        while stack:
            queue.append(stack.pop())
        return queue

    def _evaluate_postfix(self, tokens: list) -> float:
        """Accepts a postfix-notated mathematical expression, calculates it, and returns the result."""
        stack = []
        for item in tokens:
            if HelperMethods.is_number(item):
                stack.append(item)
                continue

            if item in self.operators:
                op = self.operators[item]
                required_operands = 2 if op.op_type == OpType.INFIX else 1

                if len(stack) < required_operands:
                    raise InvalidParenthesisException("Missing values inside parentheses or incomplete expression.")

                if op.op_type == OpType.INFIX:
                    b = float(stack.pop())
                    a = float(stack.pop())
                    stack.append(op.apply(a, b))
                else:
                    a = float(stack.pop())
                    stack.append(op.apply(a))
                continue

            raise UnrecognizedCharacterException(f"Unknown token in evaluator: {item}")

        if len(stack) != 1:
            if len(stack) == 0:
                raise InvalidParenthesisException("Empty parentheses are not allowed.")
            raise BasicInvalidExpressionException("Invalid expression: Stack did not resolve to a single value.")

        return float(stack.pop())
