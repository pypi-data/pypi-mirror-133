# Animated Parse Tree

|               |                   |
|---------------|-------------------|
|   Author      |   Ethan Tan       |
|   Date        |   11/12/2021      |
|   Language    |   Python (py)     |

## Description

This package is meant to provide a high-level API for programmers to visualise parse trees. The eventual goal is to animate the tokenization (extracting symbols from a string), lexing (formatting the tokens), parsing (building the parse tree) and evaluation (reducing the parse tree).

## Setup

It is extremely easy to integrate this package in your existing projects.

In the command line, run:

```console
pip install animated_parse_tree
```

## Sample Usage

### From Command Line

Then in your terminal/shell, enter:

```console
python -m animated_parse_tree
```

The output should look similar to the following:

```console
Greetings...

                "This is a utility program which aims
                    to show the beauty of parse trees
                           in a fun and engaging way"

Don't be intimidated :)
It was designed to be easy to use, yet extensible.

                                               Enjoy!
?>
```

Enter 'help' to display the help menu or 'mode' to change your current mode

### From Source Files

Then in your Python source file / Jupyter Notebook, insert:

```python
from animated_parse_tree import ParseTree

# Instantiate Parse Tree Object
t = ParseTree()

# Read a Mathematical String Expression (separated by singular whitespace characters)
t.read('1 + 2 * 3')

# Retrieve the Result
print('<<< Equation >>>')
print(t.expression, '=', t.evaluate(), end='\n\n')

# Display the Parse Tree
print('<<< Parse Tree >>>')
print(str(t))
```

The output in the terminal will look something like this:

```console
<<< Equation >>>
1 + 2 * 3 = 7

<<< Parse Tree >>>
 +
/  \
1  *
  / \
  2 3
```

## Declaring Custom Operands/Operators

A `Bundle` is simply a list of Operands and/or Operators.

To extend functionality, one simply has to register their own custom operands/operators like so:

```python
# Instantiate Parse Tree Object
t = ParseTree()

# Declare Custom Operand/Operator(s)
op = Operator(symbol='sum', func=lambda *args: sum(args), priority=Priority.PRE, kind='pre', operands=4)

# Register the Custom Operand/Operator(s)
t.register(bundle=[op])

# Use it in Expressions
t.read('sum(0.1, 2.5, 30, 49)')

# Animate all the Processes
t.animate(seconds_per_frame=1.0)

# Display the Parse Tree
print(str(t))

# Evaluate the Expression
print(t.evaluate())
```

## Current Support

* Operands
    * Integers (-1, 0, 2345)
    * Floats (0.0, 2.5, -0.77)
    * Constants (pi, e)
* Operators
    * Unary
        * Pre-fix (lg, -)
        * Post-fix (deg, !)
    * Binary
        * Pre-fix (log)
        * In-fix (+, -, *, /, ^)
    * Multi
        * Pre-fix (if)
* Parentheses
    * Unlimited nesting

### Other Features Supported

* Implicit Operator (default is higher-priority multiplication)
* Operator Overloading (maximum of 2: 1 pre-fix and 1 non-pre-fix)
* Custom Word Operands/Operators (operands/operators whose symbols are lowercase alphabetical characters)
* Custom Symbol Operands/Operators (operands/operators whose symbols are special characters)

## See Also

- [GitHub Source Code](https://github.com/ethanolx/Animated-Parse-Tree-py)
- [Full Documentation](https://github.com/ethanolx/Animated-Parse-Tree-py/wiki)
- [Python Package (PyPI)](https://pypi.org/project/animated-parse-tree)