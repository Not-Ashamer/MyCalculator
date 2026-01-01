import pytest

# Ensure imports match your folder structure exactly
from PythonFiles.Exceptions.BasicInvalidExpressionException import BasicInvalidExpressionException
from PythonFiles.Exceptions.InvalidOperatorUsageException import InvalidOperatorUsageException
from PythonFiles.Exceptions.UnrecognizedCharacterException import UnrecognizedCharacterException
from PythonFiles.Exceptions.InvalidParenthesisException import InvalidParenthesisException
from PythonFiles.CalculatorClasses.Calculator import Calculator
from PythonFiles.CalculatorClasses import OperationMethods

@pytest.fixture
def calc():
    return Calculator()

# --- BASIC TESTS ---

def test_garbage_input(calc):
    """Test that non-math characters raise the correct exception."""
    with pytest.raises(UnrecognizedCharacterException, match="The character 'h' at index 0"):
        calc.calculate("hi!")

def test_simple_addition(calc):
    assert calc.calculate("2 + 2") == 4.0

def test_simple_subtraction(calc):
    assert calc.calculate("10 - 3") == 7.0

def test_precedence(calc):
    # Multiplication (2) > Addition (1) -> 2 + 12 = 14
    assert calc.calculate("2 + 3 * 4") == 14.0
    # Parentheses (6) override everything -> 5 * 4 = 20
    assert calc.calculate("(2 + 3) * 4") == 20.0

# --- ADVANCED LOGIC TESTS ---

def test_factorial_logic():
    # Testing the static method directly
    assert OperationMethods.factorial(5) == 120
    assert OperationMethods.factorial(0) == 1

def test_sum_digits_logic():
    # 99 -> 18 -> 9
    assert OperationMethods.sum_digits(99) == 9
    # -99 -> -9
    assert OperationMethods.sum_digits(-99) == -9

def test_division_by_zero(calc):
    with pytest.raises(ZeroDivisionError):
        calc.calculate("5 / 0")

def test_negative_factorial_error(calc):
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        OperationMethods.factorial(-5)

def test_monster_expression(calc):
    exp = "-(~(3!)) + 999# * (20 @ 60) --   - 100 / 2 & (4^2 $ 50 % 6)"
    assert calc.calculate(exp) == 316.0

# --- SYNTAX & VALIDATION TESTS ---

def test_implicit_multiplication_fails(calc):
    """Test that '5(5)' is rejected (Adjacent Values)."""
    with pytest.raises(BasicInvalidExpressionException):
        calc.calculate("5(5)")
    with pytest.raises(BasicInvalidExpressionException):
        calc.calculate("(5)5")

def test_empty_parentheses_fail(calc):
    """Test that '()' is rejected."""
    with pytest.raises(InvalidParenthesisException):
        calc.calculate("()")
    with pytest.raises(InvalidParenthesisException):
        calc.calculate("5 + ()")

def test_unbalanced_parentheses_fail(calc):
    """Test mismatched parentheses."""
    with pytest.raises(InvalidParenthesisException):
        calc.calculate("(()")
    with pytest.raises(InvalidParenthesisException):
        calc.calculate("((5 + 3)")
    with pytest.raises(InvalidParenthesisException):
        calc.calculate("5 + 3)")

def test_multiple_decimals_fail(calc):
    """Test that numbers like '5.5.5' are rejected."""
    with pytest.raises(BasicInvalidExpressionException):
        calc.calculate("5.5.5")
    with pytest.raises(BasicInvalidExpressionException):
        calc.calculate("3..14")

def test_operator_at_end_of_expression(calc):
    """Test valid operator placement (End)."""
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("5 +")

def test_binary_operator_at_start(calc):
    """Test valid operator placement (Start)."""
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("* 5")

def test_consecutive_binary_operators(calc):
    """Test valid operator placement (Consecutive)."""
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("5 + * 3")

def test_invalid_tilde_usage(calc):
    """Test Tilde strict rules."""
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("~~3")

def test_postfix_after_operator(calc):
    """Test Postfix strict rules."""
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("5 + !")