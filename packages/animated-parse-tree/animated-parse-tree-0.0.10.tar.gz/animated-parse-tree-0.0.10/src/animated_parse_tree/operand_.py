from typing import Optional, Union
from .node import Node


class Operand(Node):
    def __init__(self,
                 value: Union[int, float],
                 precision: int = 3,
                 symbol: Optional[str] = None,
                 **kwargs):
        super().__init__(value=value, **kwargs)
        self.precision: int = precision
        self.symbol: str = symbol if symbol is not None else self.__str__()
        self.inner_width = len(self.symbol)
        self.width = len(self.symbol)
        self.priority = 20

    def __str__(self) -> str:
        if type(self.value) is int or len(str(self.value).split('.')[1]) <= self.precision:
            return f'{self.value:^{self.width}}'
        else:
            return f'{self.value:^{self.width}.{self.precision}f}'

    def display(self) -> str:
        return ' ' * self.left_pad + self.symbol + ' ' * self.right_pad

    def __repr__(self) -> str:
        return f'Operand({self.value})'

    def isFull(self) -> bool:
        return True
