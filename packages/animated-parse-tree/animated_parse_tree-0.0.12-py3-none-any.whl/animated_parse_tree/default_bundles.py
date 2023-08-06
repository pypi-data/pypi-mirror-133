from math import factorial, sqrt
from math import asinh, acosh, atanh
from math import sinh, cosh, tanh
from math import asin, acos, atan
from math import sin, cos, tan
from math import log10, log
from math import pi, e, tau
from typing import List, Union

from .utils.custom_functions import double_factorial, hyperfactorial, superfactorial, tetrate

from .utils.priority import Priority
from .operand_ import Operand
from .operator_ import Operator


Bundle = List[Union[Operand, Operator]]


# Basics Bundle
BASICS: Bundle = [
    Operator(symbol='+', func=lambda a, b: a + b, priority=Priority.IN_LOW, kind='in', operands=2),
    Operator(symbol='-', func=lambda a, b: a - b, priority=Priority.IN_LOW, kind='in', operands=2),
    Operator(symbol='*', func=lambda a, b: a * b, priority=Priority.IN_MID, kind='in', operands=2),
    Operator(symbol='/', func=lambda a, b: a / b, priority=Priority.IN_MID, kind='in', operands=2),
    Operator(symbol='-', func=lambda a: -a, priority=Priority.PRE, kind='pre', operands=1)
]

# Increment Bundle
INCREMENT: Bundle = [
    Operator(symbol='++', func=lambda a: a + 1, priority=Priority.POST, kind='post', operands=1),
    Operator(symbol='--', func=lambda a: a - 1, priority=Priority.POST, kind='post', operands=1)
]


# Mod Bundle
MOD: Bundle = [
    # Modulo Operator
    Operator(symbol='%', func=lambda a, b: a % b, priority=Priority.IN_MID, kind='in', operands=2),
    Operator(symbol='mod', func=lambda a, b: a % b, priority=Priority.IN_MID, kind='in', operands=2),
    Operator(symbol='modulo', func=lambda a, b: a % b, priority=Priority.IN_MID, kind='in', operands=2),

    # Modulus Operator
    Operator(symbol='abs', func=lambda a: a if a >= 0 else -a, priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='modulus', func=lambda a: a if a >= 0 else -a, priority=Priority.PRE, kind='pre', operands=1),

    # Floor Division Operator
    Operator(symbol='//', func=lambda a, b: a // b, priority=Priority.IN_MID, kind='in', operands=2)
]

# Constants Bundle
CONSTANTS: Bundle = [
    Operand(value=pi, symbol='pi'),
    Operand(value=e, symbol='e'),
    Operand(value=tau, symbol='tau'),
    Operand(value=(1 + (5 ** 0.5)) / 2, symbol='phi')
]


# Power Bundle
POWER: Bundle = [
    # Exponential Operator
    Operator(symbol='^', func=lambda a, b: a ** b, priority=Priority.IN_HIGH, kind='in', operands=2),
    Operator(symbol='**', func=lambda a, b: a ** b, priority=Priority.IN_HIGH, kind='in', operands=2),

    # Root Operator
    Operator(symbol='_/', func=lambda a: sqrt(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='_/', func=lambda a, b: b ** (1 / a), priority=Priority.IN_HIGH, kind='in', operands=2),

    # Logarithmic Operators
    Operator(symbol='log', func=lambda a, b: log(b, a), priority=Priority.PRE, kind='pre', operands=2),
    Operator(symbol='lg', func=lambda a: log10(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='ln', func=lambda a: log(a), priority=Priority.PRE, kind='pre', operands=1),

    # Tetration Operator
    Operator(symbol='^^', func=tetrate, priority=Priority.IN_HIGH, kind='in', operands=2)
]


# Trigonometry Bundle
TRIGONOMETRY: Bundle = [
    # Unit Conversion
    Operator(symbol='deg', func=lambda a: (pi / 180) * a, priority=Priority.POST, kind='post', operands=1),
    Operator(symbol='degrees', func=lambda a: (pi / 180) * a, priority=Priority.POST, kind='post', operands=1),

    # Basic Operators
    Operator(symbol='sin', func=lambda a: sin(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='sine', func=lambda a: sin(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='cos', func=lambda a: cos(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='cosine', func=lambda a: cos(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='tan', func=lambda a: tan(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='tangent', func=lambda a: tan(a), priority=Priority.PRE, kind='pre', operands=1),

    # Reciprocal Operators
    Operator(symbol='csc', func=lambda a: 1 / sin(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='sec', func=lambda a: 1 / cos(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='cot', func=lambda a: 1 / tan(a), priority=Priority.PRE, kind='pre', operands=1),

    # Inverse Operators
    Operator(symbol='asin', func=lambda a: asin(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='acos', func=lambda a: acos(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='atan', func=lambda a: atan(a), priority=Priority.PRE, kind='pre', operands=1),

    # Hyperbolic Operators
    Operator(symbol='sinh', func=lambda a: sinh(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='cosh', func=lambda a: cosh(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='tanh', func=lambda a: tanh(a), priority=Priority.PRE, kind='pre', operands=1),

    # Inverse Hyperbolic Operators
    Operator(symbol='asinh', func=lambda a: asinh(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='acosh', func=lambda a: acosh(a), priority=Priority.PRE, kind='pre', operands=1),
    Operator(symbol='atanh', func=lambda a: atanh(a), priority=Priority.PRE, kind='pre', operands=1)
]


# Factorial Bundle
FACTORIAL: Bundle = [
    # Regular Factorial Operator
    Operator(symbol='!', func=lambda a: factorial(a), priority=Priority.POST, kind='post', operands=1),

    # Subfactorial Operator
    Operator(symbol='!', func=lambda a: factorial(a) * sum(((-1) ** k) / factorial(k) for k in range(0, a + 1)), priority=Priority.PRE, kind='pre', operands=1),

    # Double Factorial Operator
    Operator(symbol='!!', func=double_factorial, priority=Priority.POST, kind='post', operands=1),

    # Superfactorial Operator
    Operator(symbol='$', func=superfactorial, priority=Priority.POST, kind='post', operands=1),

    # Hyperfactorial Operator
    Operator(symbol='#', func=hyperfactorial, priority=Priority.POST, kind='post', operands=1),
]


# Logic Bundle
LOGIC: Bundle = [
    # Operands
    Operand(value=0, symbol='false'),
    Operand(value=1, symbol='true'),

    # Boolean Operators
    Operator(symbol='~', func=lambda a: 1 if a == 0 else 0, priority=Priority.BOOLEAN_HIGH, kind='pre', operands=1),
    Operator(symbol='not', func=lambda a: 1 if a == 0 else 0, priority=Priority.BOOLEAN_HIGH, kind='pre', operands=1),
    Operator(symbol='|', func=lambda a, b: 1 if a == 1 or b == 1 else 0, priority=Priority.BOOLEAN_LOW, kind='in', operands=2),
    Operator(symbol='||', func=lambda a, b: 1 if a == 1 or b == 1 else 0, priority=Priority.BOOLEAN_LOW, kind='in', operands=2),
    Operator(symbol='or', func=lambda a, b: 1 if a == 1 or b == 1 else 0, priority=Priority.BOOLEAN_LOW, kind='in', operands=2),
    Operator(symbol='xor', func=lambda a, b: 1 if (a == 1 and b == 0) or (a == 0 and b == 1) else 0, priority=Priority.BOOLEAN_MID, kind='in', operands=2),
    Operator(symbol='&', func=lambda a, b: 1 if a == 1 and b == 1 else 0, priority=Priority.BOOLEAN_MID, kind='in', operands=2),
    Operator(symbol='&&', func=lambda a, b: 1 if a == 1 and b == 1 else 0, priority=Priority.BOOLEAN_MID, kind='in', operands=2),
    Operator(symbol='and', func=lambda a, b: 1 if a == 1 and b == 1 else 0, priority=Priority.BOOLEAN_MID, kind='in', operands=2),

    # Comparison Operators
    Operator(symbol='<', func=lambda a, b: int(a < b), priority=Priority.COMPARISON_HIGH, kind='in', operands=2),
    Operator(symbol='<=', func=lambda a, b: int(a <= b), priority=Priority.COMPARISON_HIGH, kind='in', operands=2),
    Operator(symbol='>', func=lambda a, b: int(a > b), priority=Priority.COMPARISON_HIGH, kind='in', operands=2),
    Operator(symbol='>=', func=lambda a, b: int(a >= b), priority=Priority.COMPARISON_HIGH, kind='in', operands=2),
    Operator(symbol='=', func=lambda a, b: int(a == b), priority=Priority.COMPARISON_LOW, kind='in', operands=2),
    Operator(symbol='==', func=lambda a, b: int(a == b), priority=Priority.COMPARISON_LOW, kind='in', operands=2),
    Operator(symbol='<>', func=lambda a, b: int(a != b), priority=Priority.COMPARISON_LOW, kind='in', operands=2),
    Operator(symbol='!=', func=lambda a, b: int(a != b), priority=Priority.COMPARISON_LOW, kind='in', operands=2),

    # Ternary/Conditional Operator
    Operator(symbol='if', func=lambda a, b, c: b if a == 1 else c, priority=Priority.PRE, kind='pre', operands=3),
    Operator(symbol='?', func=lambda a, b, c: b if a == 1 else c, priority=Priority.PRE, kind='pre', operands=3)
]

### FUTURE FEATURES ###

# Series Bundle
# SERIES: Bundle = [
#     Operator(symbol='sum', func=lambda a, b, c: a + b + c, priority=9)
# ]
