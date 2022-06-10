import csv

from board import Board
from pieces import Man, King, Position, Color
from moves import Move


class Game:
    board_size = 8

    def __init__(self):
        self.board = Board(Game.board_size)
        self.player_white = Player(Color.WHITE)
        self.player_black = Player(Color.BLACK)
        self.moves_counter = 0

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

    def make_move(self, move: Move):
        piece = self.board.get_field_by_position(move.start)
        for position in move:
            self.board.move_piece(piece, position.row, position.column)
            self.board.nice_print()
        for piece in move.captured_pieces:
            self.board.remove_piece(piece)
        self.board.nice_print()

    def make_partial_move(self, piece, position):
        self.board.move_piece(piece, position.row, position.column)
        self.board.nice_print()

    def end_move(self, move: Move):
        ...

    def make_move_gen(self, move: Move):
        piece = self.board.get_field_by_position(move.start)
        for position in move:
            self.board.move_piece(piece, position.row, position.column)
            yield
        for piece in move.captured_pieces:
            self.board.remove_piece(piece)
            yield


class Player:
    def __init__(self, color: Color):
        self.color = color
        self.pieces = []
        self.score = 0
        captured_pieces = []
        self.valid_moves = None

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

    def get_valid_moves(self):
        king_capturing = False
        man_capturing = False
        moves = {}
        for piece in self.pieces:
            if king_capturing and isinstance(piece, Man):
                break
            valid_moves = piece.get_valid_moves()
            if valid_moves:
                if valid_moves[0].captured_pieces:
                    if isinstance(piece, King):
                        if not king_capturing:
                            king_capturing = True
                    else:
                        if not man_capturing:
                            man_capturing = True
                else:
                    if king_capturing or man_capturing:
                        continue
                moves[piece] = valid_moves

        self.valid_moves = moves
        return moves

    def get_current_valid_moves(self, piece, jumped_positions=[]):
        moves = []
        for move in self.valid_moves[piece]:
            if jumped_positions:
                sep = len(jumped_positions) - 1
                if str(move.get_jump_positions()[:sep]) == str(jumped_positions):
                    moves.append(move)
            else:
                moves.append(move)

        self.valid_moves = {piece: moves}
        return moves

    def get_valid_next_positions(self, piece, jumped_positions=None):
        next_positions = []
        for move in self.valid_moves[piece]:
            next_positions.append(move.get_jump_positions()[len(jumped_positions)])
        return next_positions

    def get_move_from_positions(self, piece, positions):
        for move in self.valid_moves[piece]:
            if str(move.get_jump_positions()) == str(positions):
                return move

    def get_valid_first_jumps(self):
        positions = []
        for piece in self.valid_moves.keys():
            for move in self.valid_moves[piece]:
                positions.append(move.start)
        return positions

    # korunuj kamen na damu
    def coronate_piece(self, piece):
        king = King(piece.color, piece.position, piece.board)
        self.remove_piece(piece)
        piece.board.remove_piece(piece)
        self.add_piece(king)
        piece.board.add_piece(king)


if __name__ == "__main__":
    game = Game()
    game.load_game_from_CSV('saves/nacti.csv')
    game.board.nice_print()
    print(game.board.get_board())
    print(game.player_black.pieces)