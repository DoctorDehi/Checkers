from accessories import Position


class Move:
    def __init__(self, vertices: list[Position]):
        """

        :param vertices: seznam poloh: počáteční + body obratu + koncový
        """
        ...
        self.start = vertices[0]
        self.stop = vertices[-1]
        self.turnovers = vertices[1:-1]

    def get_vertices(self):
        return [self.start] + self.turnovers + [self.stop]

    def __repr__(self):
        return str(self.get_vertices())


class MoveTree:
    def __init__(self):
        self.root = None

    def add(self, node):
        if self.root is not None:
            self.root.add_descendant(node)
        else:
            self.root = node

    def add_nodes(self, nodes):
        for node in nodes:
            self.add(node)

    def to_list(self):
        if self.root:
            lst = []
            self.root.append_to_list(lst)
            return lst
        else:
            return []

    def to_move(self, node) -> Move:
        if self.root is node:
            return Move(self.root.position)
        else:
            for next_node in self.root.next_positions:
                path_to_node = next_node.to_move(node)
                if path_to_node:
                    return Move([self.root.position] + path_to_node)

    def get_end_nodes(self):
        if self.root:
            end_positions = []
            for next_position in self.root.next_positions:
                end_positions = next_position.get_end_nodes(end_positions)

        return end_positions

    def __repr__(self):
        if self.root:
            return repr(self.root)
        else:
            return "()"


class PositionNode:
    def __init__(self, position: Position, captured_pieces=None):
        self.position = position
        self.captured_pieces = captured_pieces
        self.next_positions = []

    def add_descendant(self, node):
        if isinstance(node, PositionNode):
            self.next_positions.append(node)

    def add_descendants(self, nodes):
        for node in nodes:
            self.add_descendant(node)

    def create_next_node(self, position, captured_pieces=None):
        self.add_descendant(PositionNode(position, captured_pieces))

    def to_list(self):
        node_list = [self.position]
        for position in self.next_positions:
            node_list.append(position.to_list())
        return node_list

    def to_move(self, node) -> list[Position]:
        if self is node:
            return [self.position]
        else:
            for next_node in self.next_positions:
                path_to_node = next_node.to_move(node)
                if path_to_node:
                    return [self.position] + path_to_node

    def get_end_nodes(self, end_positions):
        if self.next_positions:
            for next_position in self.next_positions:
                end_positions = next_position.get_end_nodes(end_positions)
        else:
            end_positions.append(self)
        return end_positions

    def get_next_positions(self):
        return self.next_positions

    def append_to_list(self, lst):
        lst.append(self.position)
        for position in self.next_positions:
            lst.append(position.append_to_list(lst))

    def __repr__(self):
        if not self.next_positions:
            return repr(self.position)
        else:
            repr_str = repr(self.position) + "+"
            for position in self.next_positions:
                repr_str = repr_str + ":" + repr(position)
            return repr_str
