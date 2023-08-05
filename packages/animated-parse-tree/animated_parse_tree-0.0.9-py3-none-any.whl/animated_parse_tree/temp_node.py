from .node import Node


class Temp_Node(Node):
    def __init__(self,
                 parent: Node,
                 blank: str = ' '):
        super().__init__(value=None)
        self.parent = parent
        self.width = parent.width
        self.left_pad = parent.left_pad
        self.right_pad = parent.right_pad
        self.blank: str = blank
        parent.children.append(self)

    def __str__(self):
        return self.blank * (self.left_pad + self.width + self.right_pad)

    def display(self):
        return self.__str__()

    def __repr__(self) -> str:
        return f'TempNode(width={self.width})'