from enum import Enum
from abc import ABC
from typing import Optional

from position import Position
from board import Board
from moves import MoveTree, PositionNode, Move


# VÝČTOVÝ TYP - omezený počet instancí
class Color(Enum):
    BLACK = 0
    WHITE = 1


class Piece(ABC):

    def __init__(self, color: Color, position: Position, board: Board):
        self.color = color
        self.position = position
        self.board = board

    def symbol(self) -> str:
        raise NotImplementedError("abstract method")

    def __repr__(self) -> str:
        return f'{self.symbol()}{self.color.name[0]}:{self.position}'

    def get_valid_moves(self, move_tree: MoveTree = None) -> Move:
        if not move_tree:
            move_tree = self.get_possible_moves()
        return move_tree.get_valid_moves()

    def get_possible_moves(self) -> MoveTree:
        raise NotImplementedError("abstract method")

    def _search_in_vector(
            self, vector: list[Position], current_direction: tuple[int, int], captured: Optional[list] = None
    ) -> list[list]:
        raise NotImplementedError("abstract method")

    def _gen_vector(self, direction_x: int, direction_y: int, start: Position) -> list[Position]:
        positions = []
        position = start
        row = position.row + direction_x
        column = position.column + direction_y

        while 0 <= row < self.board.get_size() and 0 <= column < self.board.get_size():
            position = Position(row, column)
            positions.append(position)
            row = position.row + direction_x
            column = position.column + direction_y
        return positions


class Man(Piece):
    directions = {
        Color.WHITE: ((1, 1), (1, -1)),
        Color.BLACK: ((-1, 1), (-1, -1))
    }

    def __init__(self, color: Color, position: Position, board: Board):
        super().__init__(color, position, board)
        self.last_move_tree = None

    def symbol(self) -> str:
        # přebarvení
        if self.color == Color.WHITE:
            return "\u2B24"
        else:
            return "\u25CB"

    def get_possible_moves(self) -> MoveTree:
        move_tree = MoveTree()
        root = PositionNode(self.position)
        move_tree.add(root)

        for direction in self.directions[self.color]:
            root.add_descendants(self._search_in_vector(
                self._gen_vector(direction[0], direction[1], self.position), direction)
            )

        self.last_move_tree = move_tree
        return move_tree

    def _search_in_vector(
            self, vector: list[Position], current_direction: tuple[int, int], captured: Optional[list] = None
    ) -> list[list]:
        if not captured:
            captured = []
        position_nodes = []
        last_piece = None
        for position in vector:
            piece = self.board.get_field_by_position(position)
            if piece == 1:
                if not last_piece and not captured:
                    position_node = PositionNode(position)
                    position_nodes.append([position_node, current_direction])
                    break
                elif not last_piece and captured:
                    break
                elif last_piece:
                    position_node = PositionNode(position, [last_piece] + captured)
                    position_nodes.append([position_node, current_direction])

                    for direction in self.directions[self.color]:
                        if current_direction[0] * -1 != direction[0] or current_direction[1] * -1 != direction[1]:
                            position_node.add_descendants(self._search_in_vector(
                                self._gen_vector(direction[0], direction[1], position),
                                direction, captured + [last_piece])
                            )
                    break
            elif piece.color == self.color:
                break
            elif last_piece:
                break
            else:
                last_piece = piece
        return position_nodes


class King(Piece):
    directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))

    def __init__(self, color: Color, position: Position, board: Board):
        super().__init__(color, position, board)
        self.last_move_tree = None

    def symbol(self) -> str:
        if self.color == Color.WHITE:
            return "\u29BF"
        else:
            return "\u29BE"

    def get_possible_moves(self) -> MoveTree:
        move_tree = MoveTree()
        root = PositionNode(self.position)
        move_tree.add(root)

        for direction in self.directions:
            root.add_descendants(self._search_in_vector(
                self._gen_vector(direction[0], direction[1], self.position), direction)
            )

        self.last_move_tree = move_tree
        return move_tree

    def _search_in_vector(
            self, vector: list[Position], current_direction: tuple[int, int], captured: Optional[list] = None
    ) -> list[list]:
        if not captured:
            captured = []
        position_nodes = []
        last_piece = None
        for position in vector:
            piece = self.board.get_field_by_position(position)
            # if field is blank
            if piece == 1 or piece == self:
                if not last_piece and not captured:
                    position_node = PositionNode(position)
                    position_nodes.append([position_node, current_direction])
                if last_piece:
                    if last_piece in captured:
                        break
                    position_node = PositionNode(position, [last_piece] + captured)
                    position_nodes.append([position_node, current_direction])

                    for direction in self.directions:
                        if current_direction[0] * -1 != direction[0] or current_direction[1] * -1 != direction[1]:
                            position_node.add_descendants(self._search_in_vector(
                                self._gen_vector(direction[0], direction[1], position),
                                direction, captured + [last_piece])
                            )
            # its own piece or there is already captured piece
            elif piece.color == self.color or last_piece:
                break
            # it's opponent's piece, potential jump
            else:
                last_piece = piece
        return position_nodes
