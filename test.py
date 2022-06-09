from pieces import King, Man, Piece
from game import Game

g = Game()
g.load_game_from_CSV("saves/tahy8.csv")

g.board.nice_print()

# for i in g.player_black.pieces + g.player_white.pieces:
#     print(i.get_valid_moves())
# moves = g.player_black.pieces[0].get_valid_moves()
# print(moves)
moves = g.player_white.pieces[0].get_valid_moves()
print(moves)
