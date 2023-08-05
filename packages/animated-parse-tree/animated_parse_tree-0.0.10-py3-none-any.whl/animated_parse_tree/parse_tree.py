from typing import Dict, List, Optional, Union, cast
from time import sleep

# Base Classes
from .node import Node
from .tree import Tree
from .operand_ import Operand
from .operator_ import Operator

# Key Components
from .tokenizer import Tokenizer
from .lexer import Lexer
from .parser import Parser

# Exceptions
from .exceptions import *

# Default Bundles
from .default_bundles import *

# Utilities
from .utils.io_utils import clear_console
from .utils.list_utils import find_element_where, index_first_element
from .utils.string_utils import simplify_expression
from string import ascii_lowercase
from termcolor import colored
from copy import copy, deepcopy


class ParseTree(Tree):
    def __init__(self,
                 bundles: List[Bundle] = [
                     BASICS,
                     CONSTANTS,
                     EXPONENTIATION,
                     TRIGONOMETRY,
                     FACTORIAL
                 ],
                 implicit_operator: Operator = Operator(
                     symbol='.', func=lambda a, b: a * b, priority=19),
                 **kwargs):
        super().__init__(**kwargs)
        self.expression = ''
        self.__last_build_expression = ''
        self.__token_lookup: Dict[str, Union[List[Operator], Operand]] = dict()
        self.__implicit_operator = implicit_operator
        self.__tokenizer = Tokenizer(token_lookup=self.__token_lookup)
        self.__lexer = Lexer(token_lookup=self.__token_lookup,
                             implicit_operator=self.__implicit_operator)
        self.__parser = Parser(
            token_lookup=self.__token_lookup, implicit_operator=self.__implicit_operator)
        for bundle in bundles:
            self.register(bundle=bundle)

    def validate_registration(self, op: Union[Operand, Operator]):
        if not (isinstance(op, Operand) or isinstance(op, Operator)):
            raise RegistrationError(
                'Attempted to register invalid token. Please ensure that your class inherits either Operand or Operator accordingly.')
        elif isinstance(op, Operand):
            symbol = op.symbol
            prev_op = self.__token_lookup.get(symbol)
            if prev_op is not None:
                raise RegistrationWarning(
                    f'Symbol \'{symbol}\' already registered with the value {str(prev_op)}. The Operand for \'{symbol}\' will be replaced to have value {str(op)}.')
        elif isinstance(op, Operator):
            num_of_operands = op.operands
            kind = op.kind

            # Operator operands
            if type(num_of_operands) is not int or num_of_operands < 1:
                raise LexingError(
                    f'Operator for {str(op)} has invalid number of operands ({num_of_operands})')

            # Operator details
            if kind == 'post':
                if num_of_operands != 1:
                    raise LexingError(
                        'Post-fix only allowed for unary operators')
            elif kind == 'in':
                if num_of_operands != 2:
                    raise LexingError(
                        'In-fix only allowed for binary operators')
            elif kind == 'pre':
                pass
            else:
                raise RegistrationError(
                    f'Unknown kind \'{kind}\' encountered for operator \'{op.symbol}\'')

            # Operator overloading
            current_op = self.__token_lookup.get(op.symbol)
            if current_op is not None:
                if type(current_op) is list and len(current_op) >= 2:
                    raise RegistrationError(
                        f'Operator \'{op.symbol}\' aready fully overloaded')
                elif type(current_op) is list and len(current_op) == 1:
                    pass

    def register(self, bundle: Bundle) -> None:
        for op in bundle:
            self.validate_registration(op)
            if isinstance(op, Operand):
                self.__token_lookup[op.symbol] = op
            elif isinstance(op, Operator):
                if op.symbol not in self.__token_lookup:
                    self.__token_lookup[op.symbol] = [op]
                elif isinstance(self.__token_lookup[op.symbol], List):
                    cast(List[Operator],
                         self.__token_lookup[op.symbol]).append(op)
            else:
                raise RegistrationError(
                    f'Unknown Operand/Operator encountered: {type(op)}')

    def lex_token(self, token: Optional[str] = None) -> Union[Operand, Operator, List[Operator]]:
        if token is not None:
            if token in self.__token_lookup:
                if isinstance(self.__token_lookup[token], List):
                    return cast(List[Operator], deepcopy(self.__token_lookup[token]))
                else:
                    return cast(Operand, deepcopy(self.__token_lookup[token]))
            raise LexingError(f'Unknown token {token} encountered')
        else:
            return deepcopy(self.__implicit_operator)

    def deregister(self, symbol: Optional[str] = None):
        if symbol is None:
            self.__token_lookup = {}
        else:
            self.__token_lookup.pop(symbol)
        return self

    def read(self, expression: str, method: Literal['replace', 'append'] = 'replace') -> Tree:
        if method == 'replace':
            self.expression = expression
        else:
            self.expression += expression
        return self

    def tokenize(self, expression: str):
        return self.__tokenizer.tokenize(expression=expression, kind='eager')

    def lex(self, tokens: List[str]):
        return self.__lexer.lex(tokens=tokens, kind='eager')

    def parse(self, token_obj_list: List):
        return self.__parser.parse(token_obj_list=token_obj_list)

    def build_sub_tree(self, token_obj_list: List):
        for token_obj in token_obj_list:
            if type(token_obj) is list:
                t = ParseTree()
                sub_root, _ = t.build_sub_tree(token_obj_list=token_obj)
                if sub_root is None:
                    raise ParsingError('Empty parenthesis encountered')
                sub_root.priority += 20
                self.insert(sub_root)
            else:
                self.insert(token_obj)
        return self.root, self.currentPointer

    def build(self):
        if self.expression.strip() != '':
            self.reset()
            tokens = self.tokenize(self.expression)
            lexed_tokens = self.lex(tokens)
            parsed_tokens = self.parse(lexed_tokens)
            self.build_sub_tree(parsed_tokens)
            self.__last_build_expression = self.expression
            return self
        else:
            raise BuildTreeError(
                'Attempted to build parse tree with empty expression')

    def __str__(self) -> str:
        if self.root is None or self.expression != self.__last_build_expression:
            self()
        return super().__str__()

    def validate_full_tree(self, node: Optional[Node]) -> None:
        if node is None:
            raise ReduceTreeError('Tree is empty')
        if not node.isFull() and isinstance(node, Operator):
            erroneous_operator = colored(node.symbol, color='red')
            actual = colored(str(len(node.children)), color='red')
            expected = node.operands
            raise ReduceTreeError(
                f'Parse tree is not full; {erroneous_operator} has {actual}/{expected} children')
        for c in node.children:
            self.validate_full_tree(node=c)

    def evaluate(self) -> Optional[Union[int, float]]:
        if self.root is None or self.expression != self.__last_build_expression:
            self()
        self.validate_full_tree(node=self.root)
        self.update(which='values')
        return self.root.value if self.root is not None else None

    def animate(self, seconds_per_frame: Union[int, float] = 2):
        return Scene(
            token_lookup=self.__token_lookup,
            implicit_operator=self.__implicit_operator,
            seconds_per_frame=seconds_per_frame
        ).animate(expression=self.expression)

    def __call__(self):
        return self.build()


class Scene:
    def __init__(self,
                 token_lookup: Dict,
                 implicit_operator: Operator,
                 seconds_per_frame: Union[int, float] = 1) -> None:
        self.token_lookup = token_lookup
        self.implicit_operator = implicit_operator
        self.seconds_per_frame = seconds_per_frame
        self.build_tree_ratio = 3
        self.reduce_tree_ratio = 3

    def stencil(self, expression, tokens=None, lexed=None, parsed=None, tree=None) -> None:
        clear_console()
        if tokens is None:
            process = 'TOKENIZATION'
        elif lexed is None:
            process = 'LEXING'
        elif parsed is None:
            process = 'PARSING'
        elif tree is None:
            process = 'BUILDING PARSE TREE'
        else:
            process = 'REDUCING PARSE TREE'
        print(f'CURRENT PROCESS: {process}')
        print()
        print(f'Expression: {expression}')
        if tokens is not None:
            print()
            print('TOKENS >>>')
            print(tokens)
        if lexed is not None:
            print()
            print('LEXED TOKENS >>>')
            print(lexed)
            print()
        if parsed is not None:
            print('PARSED TOKENS >>>')
            print(parsed)
            print()
        if tree is not None:
            print('COMPLETE PARSE TREE >>>')
            print(tree)
            print()

    def animate_tokenization(self, expression):
        tokens: List[str] = []
        for i, j, t in Tokenizer(token_lookup=self.token_lookup).tokenize(expression=expression, kind='lazy'):
            self.stencil(expression)
            print(' ' * (i + 12) + '\u2191' + ' ' * (j - i - 1) + '\u2191')
            print(' ' * (i + 12) + 'i' + ' ' * (j - i - 1) + 'j')
            print(t)
            tokens = t
            sleep(self.seconds_per_frame)
        return tokens

    def animate_lexing(self, expression, tokens):
        lexed = []
        prefix = 1
        for o, c, l, t in Lexer(token_lookup=self.token_lookup, implicit_operator=self.implicit_operator).lex(tokens=tokens, kind='lazy'):
            self.stencil(expression, tokens)
            arrow = '\u2191'
            print(' ' * prefix + f'{arrow:^{len(t) + 2}}')
            print(f'(: {o}; ): {c}')
            print(l)
            lexed = l
            sleep(self.seconds_per_frame)
            prefix += len(t) + 4
        return lexed

    def animate_parsing(self, lexed):
        return Parser(token_lookup=self.token_lookup, implicit_operator=self.implicit_operator).parse(lexed)

    def animate_building(self, expression, tokens, lexed, parsed):
        tree = ParseTree()
        for i in range(1, len(parsed) + 1):
            self.stencil(expression, tokens, lexed, parsed)
            tmp_parsed = deepcopy(parsed[:i])
            t = ParseTree()
            t.build_sub_tree(tmp_parsed)
            print(t)
            tree = t
            sleep(self.seconds_per_frame * self.build_tree_ratio)
        return tree

    def animate_reduction(self, expression, tokens, lexed, parsed, tree, tree_repr):
        reduced_tree = tree
        prev_display = ''
        for t in self.dfs_reduce(node=tree.root, tree=tree):
            if str(t) == prev_display:
                continue
            self.stencil(expression, tokens, lexed, parsed, tree_repr)
            prev_display = str(t)
            print(prev_display)
            sleep(self.seconds_per_frame * self.reduce_tree_ratio)
        self.stencil(expression, tokens, lexed, parsed, tree_repr)
        reduced_tree.root = Operand(value=reduced_tree.root())
        print(str(reduced_tree))
        return reduced_tree.root

    def dfs_reduce(self, node: Node, tree):
        for c in node.children:
            yield from self.dfs_reduce(c, tree)
        for i, c in enumerate(node.children):
            node.children[i] = Operand(value=c())
            yield tree

    def animate(self, expression):
        expression_stripped = simplify_expression(expression)
        tokens = self.animate_tokenization(expression_stripped)
        lexed = self.animate_lexing(expression_stripped, tokens)
        parsed = self.animate_parsing(lexed)
        t = self.animate_building(expression_stripped, tokens, lexed, parsed)
        complete_tree = str(t)
        result = self.animate_reduction(
            expression, tokens, lexed, parsed, t, complete_tree)
        self.stencil(expression_stripped, tokens, lexed, parsed, complete_tree)
        print('REDUCED PARSE TREE >>>')
        print(result)
        print()
        print('EVALUATION >>>')
        result = t.evaluate()
        print(expression, '=', round(result, 5))
        return result
