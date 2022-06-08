def myrepr(obj):
    return repr(obj) if obj is not None else ""


class MoveTree:
    def __init__(self):
        self.root = None

    def add(self, node, captured_pieces=None):
        if self.root is not None:
            self.root.add_descendant(node)
        else:
            self.root = PositionNode(node)

    def to_list(self):
        if self.root:
            lst = []
            self.root.append_to_list(lst)
            return lst
        else:
            return []

    def __repr__(self):
        if self.root:
            return repr(self.root)
        else:
            return "()"


class PositionNode:
    def __init__(self, position, captured_pieces=None):
        if not captured_pieces:
            captured_pieces = []
        self.position = position
        captured_pieces = captured_pieces
        self.next_positions = []

    def add_descendant(self, node):
        if isinstance(node, PositionNode):
            print(node.position)
            self.next_positions.append(node)

    def create_next_node(self, position, captured_pieces=None):
        self.add_descendant(PositionNode(position, captured_pieces))

    def to_list(self):
        node_list = [self.postion]
        for position in self.next_positions:
            node_list.append(position.to_list())
        return node_list

    def append_to_list(self, lst):
        lst.append(self.position)
        for position in self.next_positions:
            lst.append(position.append_to_list(lst))

    def __repr__(self):
        if not self.next_positions:
            return repr(self.position)
        else:
            repr_str = repr(self.position)
            for position in self.next_positions:
                repr_str = repr_str + ":" + myrepr(position)
            return repr_str
