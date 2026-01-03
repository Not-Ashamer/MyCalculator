import pytest

from PythonFiles.CalculatorClasses import OperationMethods
from PythonFiles.CalculatorClasses.Calculator import Calculator
from PythonFiles.Exceptions.BasicInvalidExpressionException import BasicInvalidExpressionException
from PythonFiles.Exceptions.InvalidOperatorUsageException import InvalidOperatorUsageException
from PythonFiles.Exceptions.InvalidParenthesisException import InvalidParenthesisException
from PythonFiles.Exceptions.UnrecognizedCharacterException import UnrecognizedCharacterException


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
    with pytest.raises(ValueError):
        OperationMethods.sum_digits(-9)


def test_division_by_zero(calc):
    with pytest.raises(ZeroDivisionError):
        calc.calculate("5 / 0")


def test_negative_factorial_error(calc):
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        OperationMethods.factorial(-5)


def test_large_expression(calc):
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


@pytest.mark.parametrize("expression, expected", [
    ("10 -- 5", 15.0),
    ("10 --- 5", 5.0),
    ("2 * -5", -10.0),
    ("-(-5)", 5.0),
    ("123#", 6.0),
    ("4!#", 6.0),
    ("10 @ 30", 20.0),
    ("100 & 50", 50.0),
    ("10 $ 20", 20.0),
    ("10 + 5 & 2", 12.0),
    ("~5", -5.0),
    ("5 + ~5", 0.0),
    ("~(3!)", -6.0),
    ("2 ^ 3 ^ 2", 64.0),
    ("4! / 4 # + (~2)", 4.0),
    ("(10 + 20) * (30 - 5) / 2 + 50 - 10", 415.0),
    ("100 -- 50 --- 25 ---- 10 ----- 5", 130.0),
    ("(3! + 2!) @ (100 #) * 5 - 20 & 50", 2.5),
    ("2 ^ 5 + 100 % 3 * 50 - ~(50 @ 10)", 112.0),
    ("(999#) + (888#) + (777#) + (666#)", 27.0),
    ("10 $ 20 $ 30 $ 40 $ 50 $ 60 $ 70", 70.0),
    ("((10 + 2) * 5) / (4 #) - 3! + ~10", -1.0),
    ("50 @ 150 @ 200 + 5 & 10 & 20 - 5", 150.0),
    ("2 ^ (3 #) + 4! / 2 - 100 % 7 * 3", 14.0),
    ("~ (5 + 5) * ~ (10 - 20) + 50 / 2", -75.0),
    ("1000 # # + 2000 # # + 5000 # # #", 8.0),
    ("(5! / 2) + (100 @ 200) - 50 $ 10", 160.0),
    ("10 + 20 * 30 - 40 / 5 + 60 % 7 ^ 2", 618.0),
    ("( ~ 5 * ~ 5 ) + ( ~ 2 * ~ 2 ) - 5!", -91.0),
    ("10 & (50 $ (20 @ (10 + 100 #)))", 10.0),
    ("1 + 2 - 3 * 4 / 5 ^ 2 % 3 # @ 4 !", 2.52),
    ("(((((1 + 1) + 1) + 1) + 1) * 10)", 50.0),
    ("500 -- 400 --- 300 ---- 200 # + 0", 602.0),
    ("(10 @ 20) + (30 @ 40) + (50 @ 60)", 105.0),
    ("3! ^ 2 + 100 % (5 #) * ~(10 - 15)", 36.0),
    ("3! - 4!", -18.0),
    ("100 & 5 $ 50", 50.0),
    ("(12 * 11) #", 6.0),
    ("5 ^ 2 % 3", 25.0),
    ("~10 @ ~30", -20.0),
    ("~ (2 ^ 3)", -8.0),
    ("4 ^ 3 ^ 2", 4096.0),
    ("10 - - - 10", 0.0),
    ("0 #", 0.0),
    ("(3! @ 4!) + (10 $ 5) - (20 & 100)", 5.0),
    ("(3!*2#+15%9)/3^(~1@3)&(0$1)", 6.0),
    ("3+~-3",6.0),
    ("~-3!",6.0),
    ("2---3!",-4.0),
    ("-1+7",6.0),
    ("-2^4",-16.0),
    ("2+--3!",8.0),
])
def test_valid_expressions(calc, expression, expected):
    """Tests any possible expression you try from pytest parametrize"""
    assert calc.calculate(expression) == expected
def test_unary_revised(calc):
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("--~--3")
    with pytest.raises(ValueError):
        calc.calculate("2--3!")
    with pytest.raises(ValueError):
        calc.calculate("~--3!")
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("~--~-3")
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("~~3")
    with pytest.raises(InvalidOperatorUsageException):
        calc.calculate("~~~3")