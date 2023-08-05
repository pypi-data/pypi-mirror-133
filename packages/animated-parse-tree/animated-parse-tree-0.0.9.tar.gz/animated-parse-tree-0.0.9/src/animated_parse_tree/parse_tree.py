from typing import Dict, List, Optional, Union, cast

# Base Classes
from .node import Node
from .tree import Tree
from .operand_ import Operand
from .operator_ import Operator

# Key Components
from .tokenizer import Tokenizer
from .lexer import Lexer
from .parser import Parser
from .scene import Scene

# Exceptions
from .exceptions import *

# Default Bundles
from .default_bundles import *

# Utilities
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
        self.token_lookup: Dict[str, Union[List[Operator], Operand]] = dict()
        for bundle in bundles:
            self.register(bundle=bundle)
        self.implicit_operator = implicit_operator

    def validate_registration(self, op: Union[Operand, Operator]):
        if not (isinstance(op, Operand) or isinstance(op, Operator)):
            raise RegistrationError(
                'Attempted to register invalid token. Please ensure that your class inherits either Operand or Operator accordingly.')
        elif isinstance(op, Operand):
            symbol = op.symbol
            prev_op = self.token_lookup.get(symbol)
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
            current_op = self.token_lookup.get(op.symbol)
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
                self.token_lookup[op.symbol] = op
            elif isinstance(op, Operator):
                if op.symbol not in self.token_lookup:
                    self.token_lookup[op.symbol] = [op]
                elif isinstance(self.token_lookup[op.symbol], List):
                    cast(List[Operator],
                         self.token_lookup[op.symbol]).append(op)
            else:
                raise RegistrationError(
                    f'Unknown Operand/Operator encountered: {type(op)}')

    def lex_token(self, token: Optional[str] = None) -> Union[Operand, Operator, List[Operator]]:
        if token is not None:
            if token in self.token_lookup:
                if isinstance(self.token_lookup[token], List):
                    return cast(List[Operator], deepcopy(self.token_lookup[token]))
                else:
                    return cast(Operand, deepcopy(self.token_lookup[token]))
            raise LexingError(f'Unknown token {token} encountered')
        else:
            return deepcopy(self.implicit_operator)

    def deregister(self, symbol: Optional[str] = None):
        if symbol is None:
            self.token_lookup = {}
        else:
            self.token_lookup.pop(symbol)
        return self

    def read(self, expression: str) -> Tree:
        self.expression = expression
        return self

    def tokenize(self, expression: str):
        return Tokenizer(token_lookup=self.token_lookup).tokenize(expression=expression, kind='eager')
    # Tokenizer
    # def tokenize(self, expression: str):
    #     token_list = []

    #     expression_simplified = simplify_expression(expression)

    #     # To check if single character is recognised
    #     digit_set = set('0123456789.')
    #     letter_set = set(ascii_lowercase)
    #     symbol_set = set(
    #         ''.join(filter(lambda s: not s.isalpha(), self.token_lookup.keys())))

    #     # To check if tokens are recognised
    #     recognised_tokens = set(self.token_lookup.keys()).union(set('(,)'))

    #     i = 0
    #     j = 1

    #     def slide_j(expression_simplified: str, current_set: set, j: int) -> int:
    #         while j < len(expression_simplified) and expression_simplified[j] in current_set:
    #             j += 1
    #         return j

    #     while j <= len(expression_simplified):
    #         char = expression_simplified[i]
    #         if char not in '(,)':
    #             if char in digit_set:
    #                 j = slide_j(expression_simplified,
    #                             current_set=digit_set, j=j)
    #             elif char in letter_set:
    #                 j = slide_j(expression_simplified,
    #                             current_set=letter_set, j=j)
    #             elif char in symbol_set:
    #                 j = slide_j(expression_simplified,
    #                             current_set=symbol_set, j=j)
    #             else:
    #                 raise TokenizationError(
    #                     expression_simplified=expression_simplified, kind='symbol', i=i, j=j)
    #         token = expression_simplified[i:j]
    #         if token in recognised_tokens or token[0] in digit_set:
    #             token_list.append(token)
    #         else:
    #             for k in range(j, i, -1):
    #                 token = expression_simplified[i:k]
    #                 if token in recognised_tokens:
    #                     token_list.append(token)
    #                     j = k
    #                     break
    #             else:
    #                 raise TokenizationError(
    #                     expression_simplified=expression_simplified, kind='token', i=i, j=j)
    #         i = j
    #         j += 1
    #     return token_list

    def lex(self, tokens: List[str]):
        return Lexer(token_lookup=self.token_lookup, implicit_operator=self.implicit_operator).lex(tokens=tokens)

    # def lex(self, tokens: List[str]):
    #     lexed_token_list: List[Union[Operand,
    #                                  Operator, List[Operator], str]] = []

    #     digit_set = set('0123456789.')

    #     open_parentheses_count = 0
    #     close_parentheses_count = 0

    #     for token in tokens:
    #         if token in '(,)':
    #             if token == '(':
    #                 open_parentheses_count += 1
    #             elif token == ')':
    #                 close_parentheses_count += 1
    #             lexed_token_list.append(token)
    #         elif token[0] in digit_set:
    #             # Normal numeric operand
    #             num = float(token) if '.' in token else int(token)
    #             lexed_token_list.append(Operand(value=num))
    #         else:
    #             token_obj = self.lex_token(token=token)
    #             if isinstance(token_obj, Operand):
    #                 lexed_token_list.append(self.lex_token(token=token))
    #             elif isinstance(token_obj, List):
    #                 if len(token_obj) == 1:
    #                     lexed_token_list.append(
    #                         cast(List[Operator], self.lex_token(token=token))[0])
    #                 else:
    #                     lexed_token_list.append(self.lex_token(token=token))
    #     if close_parentheses_count != open_parentheses_count:
    #         raise LexingError(
    #             f'{open_parentheses_count} \'(\' does not match {close_parentheses_count} \')\'')
    #     return lexed_token_list

    def parse(self, token_obj_list: List):
        return Parser(token_lookup=self.token_lookup, implicit_operator=self.implicit_operator).parse(token_obj_list=token_obj_list)

    # def parse(self, token_obj_list: List, operand_expected: bool = True, index: int = 0, depth: int = 0):
        # parsed_tokens: List = []
        # while index < len(token_obj_list):
        #     token_obj = token_obj_list[index]
        #     if token_obj == ')':
        #         operand_expected = False
        #         if depth > 0:
        #             return index, parsed_tokens, operand_expected
        #     elif token_obj == '(':
        #         if not operand_expected:
        #             parsed_tokens.append(self.lex_token())
        #         terminating_index, nested_parsed_tokens, operand_expected = self.parse(
        #             token_obj_list=token_obj_list, operand_expected=True, index=index + 1, depth=depth + 1)
        #         parsed_tokens.append(nested_parsed_tokens)
        #         index = terminating_index
        #     elif type(token_obj) is list:
        #         # Operator overloaded
        #         token_obj = find_element_where(
        #             ls=token_obj, condition=lambda el: el.kind == 'pre' if operand_expected else el.kind != 'pre')
        #         operand_expected = self.insert_token_obj(
        #             parsed_tokens=parsed_tokens, token_obj=token_obj, operand_expected=operand_expected)
        #     elif isinstance(token_obj, Operator) and token_obj.kind == 'post':
        #         operand_expected = self.insert_token_obj(
        #             parsed_tokens=parsed_tokens, token_obj=token_obj, operand_expected=operand_expected)
        #     else:
        #         operand_expected = self.insert_token_obj(
        #             parsed_tokens=parsed_tokens, token_obj=token_obj, operand_expected=operand_expected)
        #     index += 1
        # return parsed_tokens

    # def __parse_open_parenthesis(self, lexed_tokens: List, parsed_tokens: List, index: int, operand_expected: bool, depth: int):
    #     if operand_expected:
    #         pass
    #     else:
    #         # Attempt implicit operation
    #         parsed_tokens.append(self.lex_token())
    #     parsed_tokens.append('')

    # def insert_token_obj(self, parsed_tokens: List[Union[Operand, Operator]], token_obj: Union[Operand, Operator], operand_expected: bool) -> bool:
    #     if operand_expected and isinstance(token_obj, Operand):
    #         parsed_tokens.append(token_obj)
    #         return False
    #     elif operand_expected and isinstance(token_obj, Operator) and token_obj.kind == 'pre':
    #         parsed_tokens.append(token_obj)
    #         return True
    #     elif (not operand_expected) and isinstance(token_obj, Operator) and token_obj.kind == 'pre':
    #         # Implicit Multiplication
    #         parsed_tokens.append(cast(Operator, self.lex_token()))
    #         parsed_tokens.append(token_obj)
    #         return True
    #     elif (not operand_expected) and isinstance(token_obj, Operator) and token_obj.kind == 'post':
    #         prev_token_obj = parsed_tokens.pop()
    #         parsed_tokens.append(token_obj)
    #         parsed_tokens.append(prev_token_obj)
    #         return operand_expected
    #     elif (not operand_expected) and isinstance(token_obj, Operator):
    #         parsed_tokens.append(token_obj)
    #         return True
    #     elif (not operand_expected) and isinstance(token_obj, Operand):
    #         # Implicit Multiplication
    #         parsed_tokens.append(cast(Operator, self.lex_token()))
    #         parsed_tokens.append(token_obj)
    #         return False
    #     elif operand_expected and isinstance(token_obj, Operator) and token_obj.kind != 'pre':
    #         raise ParsingError(
    #             f'Expected operand but received non pre-fix operator {token_obj}')
    #     else:
    #         raise ParsingError(
    #             'Unknown error encountered. Please check your expression again.')

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
            return self
        else:
            raise BuildTreeError(
                'Attempted to build parse tree with empty expression')

    def __str__(self) -> str:
        if self.root is None:
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
        if self.root is None:
            self()
        self.validate_full_tree(node=self.root)
        self.update(which='values')
        return self.root.value if self.root is not None else None

    # def animate(self, phases: Union[str, List[str]] = 'all'):
    #     if phases == 'all':
    #         pass
    def animate(self, seconds_per_frame: int = 2) -> None:
        Scene(parse_tree_class=ParseTree, token_lookup=self.token_lookup, implicit_operator=self.implicit_operator,
              seconds_per_frame=seconds_per_frame).animate(expression=self.expression)

    def __call__(self):
        self.build()
        return self
