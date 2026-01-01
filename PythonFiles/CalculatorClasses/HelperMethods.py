from PythonFiles.Exceptions import InvalidParenthesisException


def is_number(token: str) -> bool:
    """Helper to check if a string is a valid float."""
    try:
        float(token)
        return True
    except (ValueError, TypeError):
        return False
def parentheses_balanced(tokens: list) -> bool:
    """Makes sure that all the parentheses are set and nothing is closed prematurely or left open"""
    count = 0
    for item in tokens:
        if item == "(":
            count += 1
        elif item == ")":
            count -= 1

        if count < 0:
            raise InvalidParenthesisException("ERROR: Closed Parentheses That Were Not Open")

    if count!=0:
        raise InvalidParenthesisException("ERROR: Leftover Open Parentheses")
    return True
def is_digit(char: str) -> bool:
    """
    Checks if a single character is a digit 0-9.
    Does NOT accept decimal points or negative signs.
    Used by the tokenizer to identify the start of a number.
    """
    if len(char) != 1:
        return False
    return "0" <= char <= "9"
    # Alternatively: return char.isdigit()

