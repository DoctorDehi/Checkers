from enum import Enum

from board import Board


# VÝČTOVÝ TYP - omezený počet instancí
class Color(Enum):
    BLACK = 0
    WHITE = 1


class Position:
    rowchars = 'ABCDEFGH'  # class/static attribute

    def __init__(self, row, column):
        assert 0 <= row < 8, 'Invalid row'
        assert 0 <= column < 9, 'Invalid column'
        assert (row + column) % 2 == 0, 'White square'
        self.row = row
        self.column = column

    def __repr__(self):
        return f'{Position.rowchars[self.row]}{self.column + 1}'

    # v Pythonu je lepší vyhýbat se přetížení
    @staticmethod
    def from_notation(notation: str):
        assert len(notation) == 2, 'Invalid notation'
        row = Position.rowchars.index(notation[0])
        column = int(notation[1]) - 1
        return Position(row, column)


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

    def possibleMoves(self) -> list[Move]:
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

    def possibleMoves(self) -> list[Move]:
        moves = []
        if self.color == Color.WHITE:
            move = []
            row = self.position.row+1
            column = self.position.column+1
            if self.board.field_exists(row, column):
                if self.board.is_field_occupied(row, column):
                    if self.board.get_field(row, column).color == Color.BLACK:
                        # zkontroluj pozici za ním
                        if not self.board.is_field_occupied(row+1, column+1):
                            # přidej braní do tahu, musí se uložit i figurka kterou přeskakuje?
                            ...
                            # jsi v braní, podívej se jestli můžeš brát dál, rekurze
                else:
                    # pole je volné, je přidáno do seznamu tahů
                    ...




class King(Piece):
    def __init__(self, color: Color, position: Position, board: Board):
        super().__init__(color, position, board)

    def symbol(self):
        #return "\u1F45"
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
