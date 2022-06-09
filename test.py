from pieces import King, Man, Piece
from game import Game
#
# g6 = Game()
# g6.load_game_from_CSV("saves/tahy6.csv")
# assert (str(g6.player_white.pieces[0].get_valid_moves()) == "G1+:E3+:B6:A7:G5+:D8:H6:D4+:B6:A7:H2")
#
# g7 = Game()
# g7.load_game_from_CSV("saves/tahy7.csv")
# assert (str(g7.player_white.pieces[0].get_valid_moves()) == "E1+:D2:B4+:F8+:H6:A5:F2:G3:H4")
#
# g8 = Game()
# g8.load_game_from_CSV("saves/tahy8.csv")
# assert (str(g8.player_white.pieces[0].get_valid_moves()) == "E1+:D2:B4:A5+:D8+:H4:F2:G3:H4")
#
#
g = Game()
g.load_game_from_CSV("saves/tahy1.csv")
print(g.player_white.pieces[0].get_possible_moves())
# print(g.player_white.pieces[0].get_valid_moves())
# print(g.player_white.pieces)
# print(g.player_black.pieces)
# print(g.board.get_board())
#
# print("OK")
