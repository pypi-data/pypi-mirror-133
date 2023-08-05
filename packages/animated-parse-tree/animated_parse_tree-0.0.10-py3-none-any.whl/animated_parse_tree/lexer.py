from copy import deepcopy
from typing import Dict, List, Literal, cast

from .exceptions import LexingError
from .operand_ import Operand
from .operator_ import Operator


class Lexer:
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

    def __lazy_lexing(self, tokens):
        lexed_token_list = []

        digit_set = set('0123456789.')

        open_parentheses_count = 0
        close_parentheses_count = 0

        for token in tokens:
            if token in '(,)':
                if token == '(':
                    open_parentheses_count += 1
                    lexed_token_list.append(token)
                elif token == ')':
                    close_parentheses_count += 1
                    lexed_token_list.append(token)
                else:
                    lexed_token_list.append(']')
                    lexed_token_list.append('[')
            elif token[0] in digit_set:
                # Normal numeric operand
                num = float(token) if '.' in token else int(token)
                lexed_token_list.append(Operand(value=num))
            else:
                token_obj = self.lex_token(token=token)
                if isinstance(token_obj, Operand):
                    lexed_token_list.append(self.lex_token(token=token))
                elif isinstance(token_obj, List):
                    if len(token_obj) == 1:
                        lexed_token_list.append(
                            cast(List[Operator], self.lex_token(token=token))[0])
                    else:
                        lexed_token_list.append(self.lex_token(token=token))
            yield open_parentheses_count, close_parentheses_count, lexed_token_list, token
        if close_parentheses_count != open_parentheses_count:
            raise LexingError(
                f'{open_parentheses_count} \'(\' does not match {close_parentheses_count} \')\'')

    def __eager_lexing(self, tokens: List[str]) -> List:
        token_obj_list = []
        for _, _, token_objs, _ in self.__lazy_lexing(tokens=tokens):
            token_obj_list = token_objs
        return token_obj_list

    def lex(self, tokens: List[str], kind: Literal['lazy', 'eager'] = 'eager'):
        if kind == 'lazy':
            return self.__lazy_lexing(tokens=tokens)
        elif kind == 'eager':
            return self.__eager_lexing(tokens=tokens)
        else:
            raise ValueError(f'Unknown kind \'{kind}\' received')