from enum import IntEnum


class Priority(IntEnum):
    '''
    # (Enum) Priority

    ### Boolean Operators
    NOT: BOOLEAN_HIGH
    '''
    # Boolean Operators
    BOOLEAN_LOW = 1     # or, |, ||
    BOOLEAN_MID = 3     # and, &, &&
    BOOLEAN_HIGH = 5    # not, ~

    # Comparison Operators
    COMPARISON_LOW = 7  # =, ==, <>, !=
    COMPARISON_HIGH = 9 # <, <=, >=, >

    # In-fix Operators
    IN_LOW = 11         # +, -
    IN_MID = 13         # *, x, /, //, %
    IN_HIGH = 15        # **, ^, _/, ^^

    # Pre-fix Operators
    PRE = 17            # -, sin, lg,
                        # log

    # Implicit Operator
    IMPLICIT = 19       # .

    # Post-fix Operators
    POST = 21           # !, #, $, deg

    # Arbitrary Operator
    OPERAND = 30        # 1, 2.5, pi
