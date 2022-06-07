import csv

from board import Board
from pieces import Man, King, Position, Color


class Game:
    BOARD_SIZE = 8
    PIECES_PER_PLAYER = 12

    def __init__(self):
        self.board = Board()
        self.player_white = Player(Color.WHITE)
        self.player_black = Player(Color.BLACK)

    def create_new_game(self):
        self.load_game_from_CSV('new_game.csv')

    def load_game_from_CSV(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    position = Position.from_notation(row[0])
                    if row[1] == "b":
                        self.player_black.add_piece(Man(Color.BLACK, position, self.board))
                    elif row[1] == "w":
                        self.player_white.add_piece(Man(Color.WHITE, position, self.board))
                    elif row[1] == "bb":
                        self.player_black.add_piece(King(Color.BLACK, position, self.board))
                    elif row[1] == "ww":
                        self.player_white.add_piece(King(Color.WHITE, position, self.board))

        except Exception as e:
            raise Exception("Error while loading CSV: " + str(e))


class Player:
    def __init__(self, color: Color):
        self.color = color
        self.pieces = []
        self.score = 0

    def add_piece(self, piece):
        if piece not in self.pieces:
            if isinstance(piece, King):
                self.pieces.insert(0, piece)
            else:
                self.pieces.append(piece)
            piece.board.add_piece(piece)
        else:
            print("Player already has this piece!")

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)
            piece.board.remove_piece(piece)
        else:
            print("Player does not own this piece!")

    # korunuj kamen na damu
    def coronate_piece(self, piece):
        king = King(piece.color, piece.position, piece.board)
        self.remove_piece(piece)
        piece.board.remove_piece(piece)
        self.add_piece(king)
        piece.board.add_piece(king)


if __name__ == "__main__":
    game = Game()
    game.load_game_from_CSV('nacti.csv')
    game.board.nice_print()
    print(game.board.board)
    print(game.player_black.pieces)