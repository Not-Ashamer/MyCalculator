CALCULATOR_RULES = """
CALCULATOR RULES & SYNTAX
================================================================================

1. SUPPORTED NUMBERS
   - Integers: 5, 999, -3
   - Decimals: 3.14, 0.5, -2.5
   - Note: Scientific notation (e.g., 1e5) is NOT supported.

2. OPERATORS & PRECEDENCE (Highest to Lowest)
   -----------------------------------------------------------------------------
   Lvl | Operator | Symbol | Type    | Description
   -----------------------------------------------------------------------------
    6  | Factorial|   !    | Postfix | n! (Non-negative integers only)
    6  | Digit Sum|   #    | Postfix | Sum of digits (e.g., 99# -> 18 -> 9)
    6  | Negation |   ~    | Prefix  | Negation (~5 -> -5). Strict right-side rule.
    5  | Min      |   &    | Infix   | Returns smaller value (5 & 2 -> 2)
    5  | Max      |   $    | Infix   | Returns larger value (5 $ 8 -> 8)
    5  | Avg      |   @    | Infix   | Returns average (20 @ 60 -> 40)
    4  | Modulo   |   %    | Infix   | Remainder of division (5 % 2 -> 1)
    3  | Power    |   ^    | Infix   | Exponentiation (2^3 -> 8). Right-associative.
   2.5 | Negation |   -    | Prefix  | Unary minus (-5). Weaker than ^.
    2  | Multiply |   *    | Infix   | Standard multiplication
    2  | Divide   |   /    | Infix   | Standard division
    1  | Add      |   +    | Infix   | Standard addition
    1  | Subtract |   -    | Infix   | Standard subtraction
   -----------------------------------------------------------------------------

3. SPECIAL SYNTAX RULES
   A. Minus Signs 
      - Multiple minus signs after an operator are treated as a single sign.
      - Even count = Positive (e.g., 2 -- 3 -> 2 + 3)
      - Odd count  = Negative (e.g., 2 --- 3 -> 2 - 3)
      - A minus after a number or ')' is always Subtraction (Binary).

   B. Tilde (~)
      - Must be followed immediately by a Number or '('.
      - Cannot be followed by another operator (e.g., ~~5 is Invalid).

   C. Implicit Multiplication
      - Not supported. You must use *.
      - Invalid: 5(5)
      - Valid:   5 * (5)

4. ERROR CONDITIONS
   - Division/Modulo by Zero: 5 / 0 or 5 % 0 -> Error.
   - Negative Factorial: (-5)! -> Error.
   - Decimal Factorial: 2.5! -> Error.
   - Empty Parentheses: () -> Error.
   - Unbalanced Parentheses: ((5) -> Error.
   - Root of Negative Number: -5^0.1 -> Error.
"""
