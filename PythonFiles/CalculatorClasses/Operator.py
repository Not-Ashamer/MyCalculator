from .CalculatorEnums import OpType
from . import HelperMethods
from PythonFiles.Exceptions.InvalidOperatorUsageException import InvalidOperatorUsageException


class Operator:
    def __init__(self, symbol: str, precedence: float, operation, op_type: int,
                 associativity: str = 'L',
                 # DEFAULT: Infix/Prefix usually accept a Prefix to their right (e.g. 5 + ~5)
                 accepted_right_types: list = None,
                 # DEFAULT: Infix/Postfix usually accept a Postfix to their left (e.g. 5! + 5)
                 accepted_left_types: list = None):

        self.symbol = symbol
        self.precedence = precedence
        self.operation = operation
        self.op_type = op_type
        self.associativity = associativity

        # Set defaults if None provided
        # By default, we allow standard behavior (Prefix on right, Postfix on left)
        self.accepted_right_types = accepted_right_types if accepted_right_types is not None else [OpType.PREFIX]
        self.accepted_left_types = accepted_left_types if accepted_left_types is not None else [OpType.POSTFIX]

    def apply(self, a, b=None):
        """This function is used to call the operation it's supposed to do based on how many numbers it's supposed to take"""
        if self.op_type == OpType.POSTFIX or self.op_type == OpType.PREFIX:
            return self.operation(a)
        return self.operation(a, b)

    def check_neighbors(self, left_token: str, right_token: str, operators_dict: dict) -> None:
        """
        Validates neighbors using the configuration lists (accepted_left_types / accepted_right_types).
        """

        # 1. CHECK LEFT SIDE
        # Required for: INFIX (5 + 5) and POSTFIX (5!)
        if self.op_type in [OpType.INFIX, OpType.POSTFIX]:
            # Error: Missing Token
            if left_token is None:
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Operator '{self.symbol}' is missing a value on the left."
                )

            # Check validity using accepted_left_types
            if not self._is_valid_neighbor(left_token, operators_dict, self.accepted_left_types, checking_left=True):
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Invalid token '{left_token}' before '{self.symbol}'."
                )

        # 2. CHECK RIGHT SIDE
        # Required for: INFIX (5 + 5) and PREFIX (~5)
        if self.op_type in [OpType.INFIX, OpType.PREFIX]:
            # Error: Missing Token
            if right_token is None:
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Operator '{self.symbol}' is missing a value on the right."
                )

            # Check validity using accepted_right_types
            if not self._is_valid_neighbor(right_token, operators_dict, self.accepted_right_types, checking_left=False):
                raise InvalidOperatorUsageException(
                    f"Syntax Error: Invalid token '{right_token}' after '{self.symbol}'."
                )

    def _is_valid_neighbor(self, token: str, operators_dict: dict, allowed_op_types: list, checking_left: bool) -> bool:
        """
        The universal validator.
        check_left=True  -> Validating the token to the Left (Looking for End of Value).
        check_left=False -> Validating the token to the Right (Looking for Start of Value).
        """
        if HelperMethods.is_number(token):
            return True
        if checking_left and token == ")":
            return True
        if not checking_left and token == "(":
            return True
        if token in operators_dict:
            neighbor_op = operators_dict[token]
            if neighbor_op.op_type in allowed_op_types:
                return True
        return False
    @staticmethod
    def is_postfix(token: str, operators_dict: dict) -> bool:
        return token in operators_dict and operators_dict[token].op_type == OpType.POSTFIX

    @staticmethod
    def is_prefix(token: str, operators_dict: dict) -> bool:
        return token in operators_dict and operators_dict[token].op_type == OpType.PREFIX
