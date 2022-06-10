from interface import CheckersApp
from game import Game


if __name__ == "__main__":
    game = Game()
    game.load_game_from_CSV("saves/tahy4.csv")

    piece = game.player_white.pieces[0]
    moves = piece.get_valid_moves()
    print(piece)
    print(moves)

    app = CheckersApp(game)
    app.run()
