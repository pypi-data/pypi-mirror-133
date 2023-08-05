from typing import Callable, List, Literal, Union
from .exceptions import ReduceTreeError
from .node import Node
from math import ceil


class Operator(Node):
    def __init__(self,
                 symbol: str,
                 func: Callable,
                 priority: int,
                 kind: Union[Literal['pre'], Literal['in'],
                             Literal['post']] = 'in',
                 operands: int = 2,
                 **kwargs):
        super().__init__(**kwargs)
        self.symbol: str = symbol
        self.priority = priority
        self.kind = kind
        self.operands = operands
        self.func = func
        self.width = len(symbol)
        self.inner_width = len(symbol)

    def __call__(self) -> Union[int, float]:
        if self.children is None:
            raise ReduceTreeError('Tree is not complete')
        return self.func(*map(lambda op: op.value, self.children))

    def __str__(self) -> str:
        return self.symbol

    def display(self):
        if len(self.symbol) <= (self.width - abs(self.bal_coef)):
            if self.bal_coef > 0:
                return ' ' * self.left_pad + f'{self.symbol:^{self.width - abs(self.bal_coef)}}' + ' ' * (abs(self.bal_coef) + self.right_pad)
            else:
                return ' ' * (self.left_pad + abs(self.bal_coef)) + f'{self.symbol:^{self.width - abs(self.bal_coef)}}' + ' ' * self.right_pad
        elif self.bal_coef > 0:
            return ' ' * self.left_pad + f'{self.symbol:<{self.width}}' + ' ' * self.right_pad
        elif self.bal_coef < 0:
            return ' ' * self.left_pad + f'{self.symbol:>{self.width}}' + ' ' * self.right_pad
        return ' ' * self.left_pad + f'{self.symbol:^{self.width}}' + ' ' * self.right_pad

    def __repr__(self) -> str:
        return f'Operator({self.symbol}, kind=\'{self.kind}\', operands={self.operands})'

    def isFull(self) -> bool:
        return len(self.children) == self.operands

    # def copy(self):
    #     return Operator(symbol=self.symbol, fun)
