from .OpType import OpType
from . import HelperMethods
from PythonFiles.Exceptions.InvalidOperatorUsageException import InvalidOperatorUsageException

class Operator:
    def __init__(self, symbol:str, precedence:int, operation, op_type:int):
        self.symbol = symbol
        self.precedence = precedence
        self.operation = operation
        self.op_type = op_type

    def apply(self, a, b=None):
        """This function is used to call the operation it's supposed to do based on how many numbers it's supposed to take"""
        if self.op_type == OpType.POSTFIX or self.op_type == OpType.PREFIX:
            return self.operation(a)
        return self.operation(a, b)

    def check_neighbors(self, left_token: str, right_token: str, operators_dict: dict) -> None:
        """
        Makes sure the operator only receives values it can't disprove are valid (it does not actually know
        if the operator on the left or right will return a number, but by running across every operator eventually,
        so long as every singe one is valid with incomplete information it will be valid overall).
        """

        # logic if operator is postfix
        # Rule: Must have a value to the Left. Right side doesn't matter here.
        if self.op_type == OpType.POSTFIX:
            if left_token is None or not self._is_valid_left_neighbor(left_token, operators_dict):
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Postfix operator '{self.symbol}' must follow a number or ')'."
                )

        # logic if operator is prefix
        # Rule: Must have a value to the Right. Left side doesn't matter here.
        elif self.op_type == OpType.PREFIX:
            if right_token is None or not self._is_valid_right_neighbor(right_token, operators_dict):
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Prefix operator '{self.symbol}' must precede a number or '('."
                )

        # logic for infix
        # Rule: Must have values on BOTH sides.
        elif self.op_type == OpType.INFIX:
            # 1. Check existence
            if left_token is None or right_token is None:
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Operator '{self.symbol}' is missing an operand."
                )

            # 2. Check Left (Must be number, ')', or Postfix)
            if not self._is_valid_left_neighbor(left_token, operators_dict):
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Invalid token '{left_token}' before '{self.symbol}'."
                )

            # 3. Check Right (Must be number, '(', or Prefix)
            if not self._is_valid_right_neighbor(right_token, operators_dict):
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Invalid token '{right_token}' after '{self.symbol}'."
                )


    def _is_valid_left_neighbor(self, token: str, operators_dict: dict) -> bool:
        """Checks if the token on the LEFT acts as a valid value end-point."""
        # 1. It is a closing parenthesis (which should return a number)
        if token == ")":
            return True
        # 2. It is a number
        if HelperMethods.is_number(token):
            return True
        # 3. It is a Postfix operator (e.g., 5! is a value even if you cant see the 5)
        if self.is_postfix(token, operators_dict):
            return True

        return False

    def _is_valid_right_neighbor(self, token: str, operators_dict: dict) -> bool:
        """Checks if the token on the RIGHT acts as a valid value start-point."""
        # 1. It is an opening parenthesis
        if token == "(":
            return True
        # 2. It is a number
        if HelperMethods.is_number(token):
            return True
        # 3. It is a Prefix operator (e.g., ~5 is a value even if you cant see the 5)
        if self.is_prefix(token, operators_dict):
            return True

        return False
    @staticmethod
    def is_postfix(token: str, operators_dict: dict) -> bool:
        return token in operators_dict and operators_dict[token].op_type == OpType.POSTFIX
    @staticmethod
    def is_prefix(token: str, operators_dict: dict) -> bool:
        return token in operators_dict and operators_dict[token].op_type == OpType.PREFIX

