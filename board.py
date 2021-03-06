from typing import Union

from position import Position


class Board:
    def __init__(self, size: int = 8):
        self.size = size
        self._board = [[1 if (i+j) % 2 == 0 else 0 for j in range(size)] for i in range(size)]

    def simple_print(self):
        for line in self._board:
            print(*line)

    def nice_print(self):
        print(*[" ", "A", "B", "C", "D", "E", "F", "G", "H"])
        line_count = 1
        for line in self._board:
            print_list = [line_count]
            for field in line:
                if field == 1:
                    print_list.append(u'\u25a0')
                elif field == 0:
                    print_list.append(" ")
                else:
                    print_list.append(field.symbol())
            line_count += 1
            print(*print_list)

    def field_exists(self, row: int, column: int) -> bool:
        return 0 <= row < self.size and 0 <= column < self.size

    def is_field_placeable(self, row: int, column: int) -> bool:
        return self._board[row][column] == 1

    def is_field_occupied(self, row: int, column: int) -> bool:
        return self._board[row][column] != 1 and self._board[row][column] != 0

    def get_field(self, row: int, column: int) -> Union['Piece', int, None]:
        if self.field_exists(row, column):
            return self._board[row][column]
        else:
            return None

    def get_field_by_position(self, position: Position) -> Union['Piece', int, None]:
        return self.get_field(position.row, position.column)

    def get_board(self) -> list[list]:
        return self._board

    def get_size(self) -> int:
        return self.size

    def add_piece(self, piece: 'Piece'):
        if self.is_field_placeable(piece.position.row, piece.position.column):
            self._board[piece.position.row][piece.position.column] = piece
        else:
            print("Not placable field")

    def move_piece(self, piece: 'Piece', new_row: int, new_column: int):
        if self.is_field_placeable(new_row, new_column):
            self._board[new_row][new_column] = piece
            self._board[piece.position.row][piece.position.column] = 1
            piece.position = Position(new_row, new_column)
        else:
            print("The field piece should be moved to is not placeble!")

    def remove_piece(self, piece: 'Piece'):
        self._board[piece.position.row][piece.position.column] = 1
