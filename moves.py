from position import Position


class Move:
    def __init__(self, vertices: list[Position], captured_pieces=None):
        """

        :param vertices: seznam poloh: počáteční + body obratu + koncový
        """
        ...
        self.start = vertices[0]
        self.stop = vertices[-1]
        self.turnovers = vertices[1:-1]
        self.captured_pieces = captured_pieces

    def get_vertices(self):
        return [self.start] + self.turnovers + [self.stop]

    def get_jump_positions(self):
        return self.turnovers + [self.stop]

    def __iter__(self):
        self.current = -1
        return self

    def __next__(self):
        self.current += 1
        if self.current < len(self.turnovers):
            return self.turnovers[self.current]
        elif self.current == len(self.turnovers):
            return self.stop
        else:
            raise StopIteration

    def __repr__(self):
        return str(self.get_vertices())


class MoveTree:
    def __init__(self):
        self.root = None

    def add(self, node, direction=None):
        if self.root is not None:
            self.root.add_descendant(node, direction)
        else:
            self.root = node

    def add_nodes(self, nodes):
        for node, direction in nodes:
            self.add(node, direction)

    def to_move(self, node) -> Move:
        if self.root is node:
            return Move(self.root.position, self.root.captured_pieces)
        else:
            for next_node in self.root.next_positions_to_list():
                path_to_node, captured_pieces = next_node.to_move(node)
                if path_to_node:
                    return Move([self.root.position] + path_to_node, captured_pieces)

    def get_valid_moves(self):
        moves = []
        for node in self.get_valid_end_nodes():
            moves.append(self.to_move(node))
        return moves

    def get_valid_end_nodes(self):
        if self.has_capturing_nodes():
            return self.root.get_valid_end_nodes([])
        else:
            if self.root:
                return self.root.next_positions_to_list()
            else:
                return []

    def get_end_nodes(self):
        if self.root:
            return self.root.get_end_nodes([])
        else:
            return []

    def has_capturing_nodes(self):
        if self.root:
            return self.root.has_capturing_nodes

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
    def __init__(self, position: Position, captured_pieces=None):
        self.position = position
        self.captured_pieces = captured_pieces
        self.has_descendants = False
        self.has_capturing_nodes = False
        self.next_positions = {
            (1, 1): [],
            (1, -1): [],
            (-1, 1): [],
            (-1, -1): [],
        }

    def add_descendant(self, node, direction):
        if isinstance(node, PositionNode):
            self.next_positions[direction].append(node)
            if not self.has_descendants:
                self.has_descendants = True
            if node.captured_pieces and not self.has_capturing_nodes:
                self.has_capturing_nodes = True

    def add_descendants(self, nodes):
        for node, direction in nodes:
            self.add_descendant(node, direction)

    def create_next_node(self, position, direction, captured_pieces=None):
        self.add_descendant(PositionNode(position, captured_pieces), direction)

    def to_move(self, node) -> list[Position]:
        if self is node:
            return [self.position], self.captured_pieces
        else:
            for next_node in self.next_positions_to_list():
                path_to_node, captured_pieces = next_node.to_move(node)
                if path_to_node:
                    return [self.position] + path_to_node, captured_pieces

        return [], []

    def get_valid_end_nodes(self, end_positions):
        if not self.has_descendants:
            end_positions.append(self)
            return end_positions
        else:
            for direction in self.next_positions.keys():
                grandson_capturing = self.grandson_capturing(direction)
                for node in self.next_positions[direction]:
                    if grandson_capturing:
                        if node.has_capturing_nodes:
                            end_positions = node.get_valid_end_nodes(end_positions)
                    elif self.has_capturing_nodes:
                        if node.captured_pieces:
                            end_positions = node.get_valid_end_nodes(end_positions)
                    else:
                        end_positions = node.get_valid_end_nodes(end_positions)

        return end_positions

    def get_end_nodes(self, end_positions):
        if self.next_positions_to_list():
            for next_position in self.next_positions_to_list():
                end_positions = next_position.get_end_nodes(end_positions)
        else:
            end_positions.append(self)
        return end_positions

    def grandson_capturing(self, direction):
        if self.has_capturing_nodes:
            for node in self.next_positions[direction]:
                if node.has_capturing_nodes:
                    return True
        else:
            return False

    # pomocná funkce pro přechod z listu na dict, časem nahradit, kde to půjde
    def next_positions_to_list(self):
        positions = []
        for direction in self.next_positions.keys():
            positions.extend(self.next_positions[direction])
        return positions

    def get_next_positions(self):
        return self.next_positions_to_list()

    def append_to_list(self, lst):
        lst.append(self.position)
        for position in self.next_positions_to_list():
            lst.append(position.append_to_list(lst))

    def to_list(self):
        node_list = [self.position]
        for position in self.next_positions_to_list():
            node_list.append(position.to_list())
        return node_list

    def __repr__(self):
        if not self.next_positions:
            return repr(self.position)
        else:
            repr_str = repr(self.position) + "+"
            for position in self.next_positions_to_list():
                repr_str = repr_str + ":" + repr(position)
            return repr_str
