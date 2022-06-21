import csv
import random

from board import Board
from pieces import Man, King, Position, Color
from moves import Move


class Game:
    board_size = 8

    def __init__(self):
        self.board = Board(Game.board_size)
        self.player_white = None
        self.player_black = None
        self.moves_counter = 0
        self.current_player = None
        self.winner = None
        self.load_game = False
        self.player_vs_bot = False

    def reset_game(self):
        self.board = Board(Game.board_size)
        self.player_white = Player(Color.WHITE)
        self.player_black = Player(Color.BLACK, self.player_vs_bot)
        self.moves_counter = 0
        self.current_player = self.player_white

    def create_new_game(self):
        self.reset_game()
        self.load_game_from_CSV('new_game.csv')

    def load_game_from_CSV(self, filename):
        self.reset_game()
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
            self.current_player.find_valid_moves()

        except Exception as e:
            raise Exception("Error while loading CSV: " + str(e))

    def toggle_player(self):
        if self.current_player == self.player_white:
            self.current_player = self.player_black
        else:
            self.current_player = self.player_white
        self.current_player.find_valid_moves()

    def game_over(self):
        self.winner = self.player_white if self.current_player == self.player_black else self.player_black

    def make_move(self, move: Move):
        piece = self.board.get_field_by_position(move.start)
        for position in move:
            self.board.move_piece(piece, position.row, position.column)
            # self.board.nice_print()
        self.end_move(piece, move)
        # self.board.nice_print()

    def make_partial_move(self, piece, position):
        self.board.move_piece(piece, position.row, position.column)

    def end_move(self, piece, move: Move):
        opponent = self.player_black if self.current_player == self.player_white else self.player_white
        if move.captured_pieces:
            for cap_piece in move.captured_pieces:
                self.board.remove_piece(cap_piece)
                opponent.remove_piece(cap_piece)
                self.current_player.score += 1

        # transform to king
        if move.stop.row == 0 and piece.color == Color.BLACK and isinstance(piece, Man):
            piece = self.player_black.piece_to_king(piece)
        elif move.stop.row == self.board_size-1 and piece.color == Color.WHITE and isinstance(piece, Man):
            self.player_white.piece_to_king(piece)


class Player:
    def __init__(self, color: Color, is_bot=False):
        self.color = color
        self.pieces = []
        self.score = 0
        self.valid_moves = None
        self.current_valid_moves = None
        self.is_bot = is_bot

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

    def find_valid_moves(self):
        king_capturing = False
        man_capturing = False
        moves = {}
        self.valid_moves = {}

        for piece in self.pieces:
            valid_moves = piece.get_valid_moves()
            moves[piece] = valid_moves

            if valid_moves:
                if valid_moves[0].captured_pieces:
                    if isinstance(piece, King):
                        if not king_capturing:
                            king_capturing = True
                    else:
                        if not man_capturing:
                            man_capturing = True

        # filtering only valid moves
        for piece in self.pieces:
            if king_capturing and isinstance(piece, Man):
                break
            if moves[piece]:
                if man_capturing or king_capturing:
                    if moves[piece][0].captured_pieces:
                        self.valid_moves[piece] = moves[piece]
                    elif man_capturing and isinstance(piece, King):
                        self.valid_moves[piece] = moves[piece]
                    else:
                        continue
                else:
                    self.valid_moves[piece] = moves[piece]

        self.current_valid_moves = self.valid_moves
        return self.valid_moves

    def find_current_valid_moves(self, piece, jumped_positions=[]):
        moves = []
        if not self.valid_moves.get(piece):
            return moves
        for move in self.current_valid_moves.get(piece):
            if jumped_positions:
                sep = len(jumped_positions)
                if str(move.get_jump_positions()[:sep]) == str(jumped_positions):
                    moves.append(move)
            else:
                moves.append(move)
        # rewrites valid moves to contain only possible moves for current piece
        if jumped_positions:
            self.current_valid_moves = {piece: moves}
        return moves

    def get_next_positions(self, piece, jumped_positions=None):
        if not self.valid_moves.get(piece):
            return []
        if not jumped_positions:
            index = 0
        else:
            index = len(jumped_positions)
        next_positions = []
        for move in self.current_valid_moves.get(piece):
            positions = move.get_jump_positions()
            if len(positions) > index:
                next_positions.append(positions[index])
        return next_positions

    def get_move_from_positions(self, piece, positions):
        for move in self.valid_moves[piece]:
            if str(move.get_jump_positions()) == str(positions):
                return move

    # korunuj kamen na damu
    def piece_to_king(self, piece):
        king = King(piece.color, piece.position, piece.board)
        self.remove_piece(piece)
        piece.board.remove_piece(piece)
        self.add_piece(king)
        piece.board.add_piece(king)
        return piece

    def get_random_move(self):
        self.find_valid_moves()
        piece_moves = random.choice(list(self.valid_moves.values()))
        return random.choice(piece_moves)

    def get_color_text(self):
        return "White" if self.color == Color.WHITE else "Black"


if __name__ == "__main__":
    game = Game()
    game.load_game_from_CSV('saves/nacti.csv')
    game.board.nice_print()
    print(game.board.get_board())
    print(game.player_black.pieces)
