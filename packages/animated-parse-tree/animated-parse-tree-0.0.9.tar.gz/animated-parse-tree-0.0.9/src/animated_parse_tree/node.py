from abc import abstractmethod
from typing import Any, List, Optional
from math import ceil


class Node:
    def __init__(self,
                 value=None):
        self.parent: Optional[Node] = None
        self.children: List[Node] = []
        self.value: Any = value
        self.height: int = 1
        self.priority: int = -1
        self.inner_width: int = 0
        self.width: int = 0
        self.bal_coef: int = 0
        self.left_pad: int = 0
        self.right_pad: int = 0

    @abstractmethod
    def isFull(self) -> bool:
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        pass

    def __lt__(self, otherNode) -> bool:
        return self.priority < otherNode.priority

    def __le__(self, otherNode) -> bool:
        return self.priority <= otherNode.priority

    def __gt__(self, otherNode) -> bool:
        return self.priority > otherNode.priority

    def __ge__(self, otherNode) -> bool:
        return self.priority >= otherNode.priority

    def __call__(self) -> Any:
        return self.value

    @abstractmethod
    def __str__(self) -> str:
        pass

    def display(self) -> str:
        return str(self.value)

    def get_balance_coefficient(self) -> int:
        last_child = self.children[-1]
        right_bal_coef = last_child.bal_coef
        right_space = ceil((last_child.width - abs(right_bal_coef) - 1) / 2) + max(right_bal_coef, 0)

        first_child = self.children[0]
        left_bal_coef = first_child.bal_coef
        left_space = (first_child.width - abs(left_bal_coef) - 1) // 2 + min(left_bal_coef, 0)

        return right_space - left_space

    def branch(self, branch_symbol: str) -> str:
        if len(self.children) == 0:
            return f'{branch_symbol:^{self.width}}'
        left_space = (self.children[0].width - 1) // 2
        right_space = (self.children[-1].width - 1) - ((self.children[-1].width - 1) // 2)
        diff = right_space - left_space
        if len(branch_symbol) <= (self.width - abs(diff)):
            if diff > 0:
                return f'{branch_symbol:^{self.width - abs(diff)}}' + ' ' * abs(diff)
            else:
                return ' ' * abs(diff) + f'{branch_symbol:^{self.width - abs(diff)}}'
        elif diff > 0:
            return f'{branch_symbol:<{self.width}}'
        elif diff < 0:
            return f'{branch_symbol:>{self.width}}'
        return f'{branch_symbol:^{self.width}}'