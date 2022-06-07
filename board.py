class Board:
    def __init__(self, size=8):
        self.board = [[1 if (i+j) % 2 == 0 else 0 for j in range(size)] for i in range(size)]

    def simple_print(self):
        for radek in self.board:
            print(*radek)

    def nice_print(self):
        print(*[" ", "A", "B", "C", "D", "E", "F", "G", "H"])
        pocet_radek = 1
        for radek in self.board:
            print_list = [pocet_radek]
            for prvek in radek:
                if prvek == 1:
                    print_list.append(u'\u25a0')
                elif prvek == 0:
                    print_list.append(" ")
                else:
                    print_list.append(prvek.symbol())
            pocet_radek += 1
            print(*print_list)

    def is_field_placeable(self, row, column):
        return self.board[row][column] == 1

    def add_piece(self, piece):
        if self.is_field_placeable(piece.position.row, piece.position.column):
            self.board[piece.position.row][piece.position.column] = piece
        else:
            raise Exception("Not placable field")

    def move_piece(self, piece, new_row, new_column):
        if self.is_field_placeable(new_row, new_column):
            self.board[new_row][new_column] = piece
            self.board[piece.position.row][piece.position.column] = 1
        else:
            raise Exception("The field piece should be moved to is not placeble!")

    def remove_piece(self, piece):
        self.board[piece.position.row][piece.position.column] = 1
