from enum import Enum

from position import Position
from board import Board
from moves import MoveTree, PositionNode


# VÝČTOVÝ TYP - omezený počet instancí
class Color(Enum):
    BLACK = 0
    WHITE = 1


class Move:
    def __init__(self, vertices: list[Position]):
        """

        :param vertices: seznam poloh: počáteční + body obratu + koncový
        """
        ...


class Piece:
    def __init__(self, color: Color, position: Position, board: Board):
        self.color = color
        self.position = position
        self.board = board

    def symbol(self):
        raise NotImplementedError("abstract method")

    def __repr__(self):
        return f'{self.symbol()}{self.color.name[0]}:{self.position}'

    def get_valid_moves(self) -> MoveTree:
        raise NotImplementedError("abstract method")

    def _check_for_move(self, next_position, r, step, column, last, captured) -> (PositionNode, list, bool):
        raise NotImplementedError("abstract method")

    def _search_left_moves(self, start, stop, step, left, direction, captured=None) -> PositionNode:
        if not captured:
            captured = []
        next_positions = []
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            next_positions, last, should_break = self._check_for_move(next_positions, r, step, left, last, captured, direction)
            if should_break:
                break
            left -= 1
        return next_positions

    def _search_right_moves(self, start, stop, step, right, direction, captured=None) -> PositionNode:
        if not captured:
            captured = []
        next_positions = []
        last = []
        for r in range(start, stop, step):
            if right >= self.board.get_size():
                break
            next_positions, last, should_break = self._check_for_move(next_positions, r, step, right, last, captured, direction)
            if should_break:
                break
            right += 1
        return next_positions


class Man(Piece):
    def __init__(self, color: Color, position: Position, board: Board):
        super().__init__(color, position, board)

    def symbol(self):
        # přebarvení
        if self.color == Color.WHITE:
            return "\u2B24"
        else:
            return "\u25CB"

    def get_valid_moves(self) -> MoveTree:
        move_tree = MoveTree()
        root = PositionNode(self.position)
        move_tree.add(root)

        left = self.position.column - 1
        right = self.position.column + 1
        row = self.position.row

        if self.color == Color.BLACK:
            move_tree.add_nodes(self._search_left_moves(row - 1, max(row - 3, -1), -1, left, direction="dl"))
            move_tree.add_nodes(self._search_right_moves(row - 1, max(row - 3, -1), -1, right, direction="dr"))

        elif self.color == Color.WHITE:
            board_size = self.board.get_size()
            move_tree.add_nodes(self._search_left_moves(row + 1, min(row + 3, board_size), 1, left, direction="ul"))
            move_tree.add_nodes(self._search_right_moves(row + 1, min(row + 3, board_size), 1, right, direction="ur"))

        return move_tree

    def _check_for_move(self, next_positions, r, step, column, last, captured, direction) -> (PositionNode, list, bool):
        """
            Returns next PositionNode with possible child nodes, last and boolean that says, if loop should break
        """
        current = self.board.get_field(r, column)
        if current == 1:
            position = Position(r, column)
            if captured and not last:
                return next_positions, last, True
            # else if captured and last
            elif captured:
                next_position = PositionNode(position, captured_pieces=last + captured)
            # not captured
            else:
                next_position = PositionNode(position, captured_pieces=last)

            next_positions.append(next_position)

            if last:
                if step == -1:
                    row = max(r - 3, 0)
                    dv = "d"
                else:
                    row = min(r + 3, self.board.get_size())
                    dv = "u"
                next_position.add_descendants(
                    self._search_left_moves(r + step, row, step, column - 1, captured=last, direction=dv + "l")
                )
                next_position.add_descendants(
                    self._search_right_moves(r + step, row, step, column + 1, captured=last, direction=dv + "l")
                )
            return next_positions, last, True
        elif current.color == self.color:
            return next_positions, last, True
        else:
            last = [current]
            return next_positions, last, False


class King(Piece):
    def __init__(self, color: Color, position: Position, board: Board):
        super().__init__(color, position, board)

    def symbol(self):
        # return "\u1F45"
        if self.color == Color.WHITE:
            return "\u29BF"
        else:
            return "\u29BE"

    def get_valid_moves(self) -> MoveTree:
        move_tree = MoveTree()
        root = PositionNode(self.position)
        move_tree.add(root)

        left = self.position.column - 1
        right = self.position.column + 1
        row = self.position.row
        board_size = self.board.get_size()

        move_tree.add_nodes(self._search_left_moves(row - 1, -1, -1, left, direction="dl"))
        move_tree.add_nodes(self._search_right_moves(row - 1, -1, -1, right, direction="dr"))
        move_tree.add_nodes(self._search_left_moves(row + 1, board_size, 1, left, direction="ul"))
        move_tree.add_nodes(self._search_right_moves(row + 1, board_size, 1, right, direction="ur"))

        return move_tree

    def _check_for_move(self, next_positions, r, step, column, last, captured, direction) -> (PositionNode, bool):
        """
            Returns next list of PositionNodes with possible child nodes, last and boolean that says, if loop should break
        """
        current = self.board.get_field(r, column)
        if current == 1:
            position = Position(r, column)
            print(position)
            if str(position) == "C3":
                print(last, captured)
            if captured and not last:
                return next_positions, last, False

            next_position = PositionNode(position, captured_pieces=captured + last)

            next_positions.append(next_position)

            if last:
                if direction != "dr":
                    next_position.add_descendants(
                        self._search_left_moves(r + step, self.board.get_size(), step, column - 1, captured=last, direction="ul")
                    )
                if direction != "dl":
                    next_position.add_descendants(
                        self._search_right_moves(r + step, self.board.get_size(), step, column + 1, captured=last, direction="ur")
                    )
                if direction != "ur":
                    next_position.add_descendants(
                        self._search_left_moves(r - step, 0, -step, column - 1, captured=last, direction="dl")
                    )
                if direction != "ul":
                    next_position.add_descendants(
                        self._search_right_moves(r - step, 0, -step, column + 1, captured=last, direction="dr")
                    )

            return next_positions, last, False
        # if there are two pieces without blank field
        elif last:
            return next_positions, last, True
        elif current.color == self.color:
            return next_positions, last, True
        # last is assigned only if there is opponent's piece
        else:
            last = [current]
            return next_positions, last, False


if __name__ == '__main__':
    """
    print(Color.BLACK)
    print(Color.BLACK.name)
    print(Color.BLACK.value)
    print(Color.BLACK == Color.BLACK)

    p1 = Position(0, 5)
    print(p1)
    p2 = Position.from_notation('A1')
    print(p2)
    """

    b = Board()
    m = Man(Color.WHITE, Position.from_notation("A1"), b)
    k = King(Color.WHITE, Position.from_notation("A1"), b)
    print(k)
