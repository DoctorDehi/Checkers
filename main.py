from interface import CheckersApp
from game import Game


if __name__ == "__main__":
    game = Game()
    game.load_game_from_CSV("new_game.csv")
    app = CheckersApp(game)
    app.run()
