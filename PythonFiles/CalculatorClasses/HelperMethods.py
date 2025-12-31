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
            return False

    return count == 0
