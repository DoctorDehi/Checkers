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

    def possibleMove(self) -> list[Move]:
        raise NotImplementedError("abstract method")


class Man(Piece):
    def __init__(self, color: Color, position: Position, board: Board):
        super().__init__(color, position, board)

    def symbol(self):
        # přebarvení
        if self.color == Color.WHITE:
            return "\u2B24"
        else:
            return "\u25CB"

    def get_valid_moves(self):
        move_tree = MoveTree()
        root = PositionNode(self.position)
        move_tree.add(root)

        left = self.position.column - 1
        right = self.position.column + 1
        row = self.position.row

        if self.color == Color.BLACK:
            move_tree.add(self._search_left_moves(row - 1, max(row - 3, -1), -1, self.color, left))
            move_tree.add(self._search_right_moves(row - 1, max(row - 3, -1), -1, self.color, right))

        elif self.color == Color.WHITE:
            board_size = self.board.get_size()
            move_tree.add(self._search_left_moves(row + 1, min(row + 3, board_size), 1, self.color, left))
            move_tree.add(self._search_right_moves(row + 1, min(row + 3, board_size), 1, self.color, right))

        return move_tree

    def _search_left_moves(self, start, stop, step, color, left, skipped=None):
        if not skipped:
            skipped = []
        next_position = None

        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board.get_field(r, left)
            if not current:
                continue
            elif current == 1:
                position = Position(r, left)

                if skipped and not last:
                    break
                elif skipped:
                    next_position = PositionNode(position, captured_pieces=last + skipped)
                else:
                    next_position = PositionNode(position, captured_pieces=last)

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, self.board.get_size())
                    next_position.add_descendant(
                        self._search_left_moves(r + step, row, step, color, left - 1, skipped=last)
                    )
                    next_position.add_descendant(
                        self._search_right_moves(r + step, row, step, color, left + 1, skipped=last)
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return next_position

    def _search_right_moves(self, start, stop, step, color, right, skipped=None):
        if not skipped:
            skipped = []
        next_position = None

        last = []
        for r in range(start, stop, step):
            if right >= self.board.get_size():
                break

            current = self.board.get_field(r, right)
            if not current:
                continue
            elif current == 1:
                position = Position(r, right)
                if skipped and not last:
                    break
                elif skipped:
                    next_position = PositionNode(position, captured_pieces=last + skipped)
                else:
                    next_position = PositionNode(position, captured_pieces=last)

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, self.board.get_size())
                    next_position.add_descendant(
                        self._search_left_moves(r + step, row, step, color, right - 1, skipped=last)
                    )
                    next_position.add_descendant(
                        self._search_right_moves(r + step, row, step, color, right + 1, skipped=last)
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return next_position

    def possibleMove(self) -> list[Move]:
        moves = []
        if self.color == Color.WHITE:
            increment = 1
        else:
            increment = -1
        move = []
        row = self.position.row + increment
        column = self.position.column + 1
        if self.board.field_exists(row, column):
            if self.board.is_field_occupied(row, column):
                if self.board.get_field(row, column).color != self.color:
                    # zkontroluj pozici za ním
                    if not self.board.is_field_occupied(row + increment, column + 1):
                        # přidej braní do tahu, musí se uložit i figurka kterou přeskakuje?
                        ...
                        # jsi v braní, podívej se jestli můžeš brát dál, rekurze
            else:
                # pole je volné, je přidáno do seznamu tahů
                ...

        return moves


class King(Piece):
    def __init__(self, color: Color, position: Position, board: Board):
        super().__init__(color, position, board)

    def symbol(self):
        # return "\u1F45"
        if self.color == Color.WHITE:
            return "\u29BF"
        else:
            return "\u29BE"


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
