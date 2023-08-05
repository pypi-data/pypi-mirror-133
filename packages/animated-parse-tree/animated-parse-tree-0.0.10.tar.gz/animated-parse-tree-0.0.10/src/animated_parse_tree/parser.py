from copy import deepcopy
from .operand_ import Operand
from .operator_ import Operator
from .exceptions import LexingError, ParsingError
from .utils.list_utils import *
from typing import Dict, List, cast, Union


class Parser:
    def __init__(self,
                 token_lookup: Dict,
                 implicit_operator: Operator) -> None:
        self.token_lookup = token_lookup
        self.implicit_operator = implicit_operator

    def lex_token(self, token=None):
        if token is not None:
            if token in self.token_lookup:
                if isinstance(self.token_lookup[token], List):
                    return cast(List[Operator], deepcopy(self.token_lookup[token]))
                else:
                    return cast(Operand, deepcopy(self.token_lookup[token]))
            raise LexingError(f'Unknown token {token} encountered')
        else:
            return deepcopy(self.implicit_operator)

    def parse(self, token_obj_list: List, operand_expected: bool = True, index: int = 0, depth: int = 0):
        parsed_tokens: List = []
        while index < len(token_obj_list):
            token_obj = token_obj_list[index]
            if token_obj == ')':
                operand_expected = False
                if depth > 0:
                    return index, parsed_tokens, operand_expected
            elif token_obj == '(':
                if not operand_expected:
                    parsed_tokens.append(self.lex_token())
                terminating_index, nested_parsed_tokens, operand_expected = self.parse(
                    token_obj_list=token_obj_list, operand_expected=True, index=index + 1, depth=depth + 1)
                parsed_tokens.append(nested_parsed_tokens)
                index = terminating_index
            elif token_obj == ']':
                if depth > 0:
                    return index, parsed_tokens, operand_expected
            elif token_obj == '[':
                terminating_index, nested_parsed_tokens, operand_expected = self.parse(
                    token_obj_list=token_obj_list, operand_expected=True, index=index + 1, depth=depth + 1)
                parsed_tokens.append(nested_parsed_tokens)
                index = terminating_index
            elif type(token_obj) is list:
                # Operator overloaded
                token_obj = find_element_where(
                    ls=token_obj, condition=lambda el: el.kind == 'pre' if operand_expected else el.kind != 'pre')
                operand_expected = self.insert_token_obj(
                    parsed_tokens=parsed_tokens, token_obj=token_obj, operand_expected=operand_expected)
            elif isinstance(token_obj, Operator) and token_obj.kind == 'post':
                operand_expected = self.insert_token_obj(
                    parsed_tokens=parsed_tokens, token_obj=token_obj, operand_expected=operand_expected)
            else:
                operand_expected = self.insert_token_obj(
                    parsed_tokens=parsed_tokens, token_obj=token_obj, operand_expected=operand_expected)
            index += 1
        return parsed_tokens

    def insert_token_obj(self, parsed_tokens: List[Union[Operand, Operator]], token_obj: Union[Operand, Operator], operand_expected: bool) -> bool:
        if operand_expected and isinstance(token_obj, Operand):
            parsed_tokens.append(token_obj)
            return False
        elif operand_expected and isinstance(token_obj, Operator) and token_obj.kind == 'pre':
            parsed_tokens.append(token_obj)
            return True
        elif (not operand_expected) and isinstance(token_obj, Operator) and token_obj.kind == 'pre':
            # Implicit Multiplication
            parsed_tokens.append(cast(Operator, self.lex_token()))
            parsed_tokens.append(token_obj)
            return True
        elif (not operand_expected) and isinstance(token_obj, Operator) and token_obj.kind == 'post':
            prev_token_obj = parsed_tokens.pop()
            parsed_tokens.append(token_obj)
            parsed_tokens.append(prev_token_obj)
            return operand_expected
        elif (not operand_expected) and isinstance(token_obj, Operator):
            parsed_tokens.append(token_obj)
            return True
        elif (not operand_expected) and isinstance(token_obj, Operand):
            # Implicit Multiplication
            parsed_tokens.append(cast(Operator, self.lex_token()))
            parsed_tokens.append(token_obj)
            return False
        elif operand_expected and isinstance(token_obj, Operator) and token_obj.kind != 'pre':
            raise ParsingError(
                f'Expected operand but received non pre-fix operator {token_obj}')
        else:
            raise ParsingError(
                'Unknown error encountered. Please check your expression again.')
