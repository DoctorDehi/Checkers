class Board:
    def __init__(self, size):
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
                    print_list.append(prvek)
            pocet_radek += 1
            print(*print_list)

    def load_piece(self, piece):
        self.board[piece.position.row()[piece.position.column()]] = piece.symbol()
