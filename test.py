from pieces import King, Man, Piece
from game import Game

g = Game()
g.load_game_from_CSV("saves/tahy5.csv")

g.board.nice_print()

