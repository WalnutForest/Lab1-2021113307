import string


class My_Edge:
    def __init__(self, node1: string, node2: string, weight: int):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __str__(self) -> str:
        return f"Edge({self.node1}, {self.node2}, {self.weight})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.node1 == other.node1 and self.node2 == other.node2
