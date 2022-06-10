from pieces import King, Man, Piece
from game import Game
from position import Position
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
g.load_game_from_CSV("saves/tahy4.csv")
g.board.nice_print()
moves = g.player_white.find_valid_moves()
piece = g.player_white.pieces[0]
print(g.player_white.get_valid_next_positions(piece))
g.player_white.find_current_valid_moves(piece, [Position.from_notation("F6")])
print(g.player_white.get_valid_next_positions(piece))
g.player_white.find_current_valid_moves(piece, [Position.from_notation("F6"), Position.from_notation("H8")])
print(g.player_white.get_valid_next_positions(piece))
print(moves)
print(g.player_white.valid_moves)

print()
print(g.player_black.find_valid_moves())
print(g.player_black.get_random_move())
print(g.player_white.find_valid_moves())
print(g.player_white.get_random_move())
# move = moves[piece][0]
# print(g.player_white.get_valid_next_positions(piece))
# for i in g.make_move_gen(move):
#     g.board.nice_print()



# node = move_tree.root.get_next_positions()[0].get_next_positions()[1]
# end_nodes = move_tree.get_end_nodes()
# for i in end_nodes:
#     print(i.captured_pieces)

# print(g.player_white.pieces[0].get_valid_moves())
# print(g.player_white.pieces)
# print(g.player_black.pieces)
# print(g.board.get_board())
#
# print("OK")
