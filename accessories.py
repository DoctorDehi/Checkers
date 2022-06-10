class Position:
    colchars = 'ABCDEFGH'  # class/static attribute

    def __init__(self, row, column):
        assert 0 <= row < 8, 'Invalid row'
        assert 0 <= column < 8, 'Invalid column'
        assert (row + column) % 2 == 0, 'White square'
        self.row = row
        self.column = column

    def __repr__(self):
        return f'{Position.colchars[self.column]}{self.row + 1}'

    # v Pythonu je lepší vyhýbat se přetížení
    @staticmethod
    def from_notation(notation: str):
        assert len(notation) == 2, 'Invalid notation'
        row = int(notation[1]) - 1
        column = Position.colchars.index(notation[0])
        return Position(row, column)
