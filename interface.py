from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.properties import OptionProperty, BooleanProperty
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from enum import Enum

from pieces import Man, King, Position


class SquareColor(Enum):
    BLACK = 0
    LIGHT = 1


class Square(Button):
    piece = OptionProperty("None", options=["None", "White", "Black", "WhiteK", "BlackK"])

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.scolor = SquareColor.BLACK if (self.row + self.column) % 2 == 0 else SquareColor.LIGHT
        super().__init__(text=self.notation())
        self.size = (0, 0)
        self.selectable = False
        self.bind(size=self.repaint)
        self.bind(piece=self.repaint)

    def repaint(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.scolor == SquareColor.LIGHT:
                Color(0.99, 0.84, 0.57)
            else:
                Color(0.35, 0.2, 0.12)
            Rectangle(pos=self.pos, size=self.size)

            if self.piece != "None":

                if self.piece in ["Black", "BlackK"]:
                    Color(0, 0, 0)
                else:
                    Color(1, 1, 1)

                Ellipse(pos=(self.x + self.width // 6, self.y + self.height // 6),
                        size=(2 * self.width // 3, 2 * self.height // 3))

                if self.piece in ["BlackK", "WhiteK"]:
                    Color(0.45, 0.45, 0.45)

                    Line(pos=(self.x + self.width // 6, self.y + self.height // 6),
                        ellipse=(
                        self.x + self.width // 3, self.y + self.height // 3, self.width // 3, self.height // 3),
                        width=1.5)

            if self.selectable:
                Color(0, 1, 0)

                Ellipse(pos=(self.x + self.width // 2.6, self.y + self.height // 2.6),
                        size=(2 * self.width // 8, 2 * self.height // 8))

    def on_press(self):
        self.parent.square_clicked(self)

    def notation(self):
        return f"{'ABCDEFGH'[self.column]}{self.row + 1}"


class BoardWidget(GridLayout):
    squares = []

    def __init__(self, app, **kwargs):
        super(BoardWidget, self).__init__(**kwargs)
        self.game = app.game
        self.info = app.info
        self.current_piece = None
        self.in_move = False
        self.jumped_positions = []
        self.next_positions = []

    def add_widget(self, widget, *args, **kwargs):
        super().add_widget(widget)

    def create_board(self):
        self.squares = []
        size = self.game.board.get_size()
        for row in range(size):
            irow = []
            for col in range(size):
                square = Square(row, col)
                irow.append(square)
                self.add_widget(square)
            self.squares.append(irow)

    def square_clicked(self, square):
        player = self.game.current_player
        if square.piece != "None" and not self.jumped_positions:
            piece = self.game.board.get_field(square.row, square.column)
            if piece.color == player.color:
                player.find_valid_moves()
                self.next_positions = player.get_next_positions(piece, self.jumped_positions)
                self.current_piece = piece

        elif self.current_piece:
            for position in self.next_positions:
                if square.row == position.row and square.column == position.column:
                    self.game.make_partial_move(self.current_piece, position)
                    self.jumped_positions.append(position)
                    player.find_current_valid_moves(self.current_piece, self.jumped_positions)
                    self.next_positions = player.get_next_positions(self.current_piece, self.jumped_positions)
                    # move is done
                    if not self.next_positions:
                        move = player.get_move_from_positions(self.current_piece, self.jumped_positions)
                        self.game.end_move(self.current_piece, move)
                        self.jumped_positions.clear()
                        self.game.toggle_player()
                        if not self.game.current_player.valid_moves:
                            self.game_over(winner=player)
                        else:
                            self.info.toggle_player()
                    break
        self.draw_board()

    def game_over(self, winner):
        self.info.game_over(winner)

    def draw_board(self):
        board_size = self.game.board.get_size()
        for row in range(board_size):
            for column in range(board_size):
                piece = self.game.board.get_field(row, column)
                if piece == 0 or piece == 1:
                    color = "None"
                elif piece in self.game.player_white.pieces:
                    if isinstance(piece, Man):
                        color = "White"
                    else:
                        color = "WhiteK"
                else:
                    if isinstance(piece, Man):
                        color = "Black"
                    else:
                        color = "BlackK"

                self.squares[row][column].piece = color
                self.squares[row][column].selectable = False
                self.squares[row][column].repaint()

        for position in self.next_positions:
            self.squares[position.row][position.column].selectable = True
            self.squares[position.row][position.column].repaint()


class InfoWidget(GridLayout):
    player = BooleanProperty(True)

    def __init__(self, game):
        super().__init__(cols=2)
        self.add_widget(Label(text="Current player: "))
        self.player_label = Label(text="White" if self.player else "Black")
        self.winner_label = Label(text="")
        self.player = True
        self.add_widget(self.player_label)
        self.add_widget(self.winner_label)
        self.bind(player=self.player_changed)
        self.game = game

    def toggle_player(self):
        self.player = not self.player
        self.parent.next_positions = []

    def player_changed(self, *args):
        self.player_label.text = "White" if self.player else "Black"
        self.player_label.color = (1, 1, 1) if self.player else (0.5, 0.5, 0.5)

    def game_over(self, winner):
        self.winner_label.text = "Player  " + self.player_label.text + " won!"


class ScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManager, self).__init__(**kwargs)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.button = Button(text="New Game", font_size = 32,)
        self.button.bind(on_release = self.screen_transition)
        self.add_widget(self.button)

    def screen_transition(self, *args):
        self.manager.current = "Checkers"


class GameScreen(Screen):
    def __init__(self, game, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="horizontal")
        self.squares = []
        self.game = game
        self.surrender_btn = Button(text = "Surrender", font_size = 32, background_color = (0,255,255,1))
        self.surrender_btn.bind(on_release = self.screen_transition)
        self.info = InfoWidget(self.game)
        self.info.add_widget(self.surrender_btn)
        self.board = BoardWidget(self, cols=8, orientation="lr-bt")
        self.board.create_board()
        self.board.draw_board()
        self.layout.add_widget(self.board)
        self.layout.add_widget(self.info)
        self.game.current_player.find_valid_moves()
        self.add_widget(self.layout)

    def screen_transition(self, **args):
        self.manager.current = "Victor"
        
    
    """    
    def start_game(self, instance):
        layout = BoxLayout(orientation="horizontal")
        self.info = InfoWidget(self.game)
        self.board = BoardWidget(self, cols=8, orientation="lr-bt")
        self.board.create_board()
        layout.add_widget(self.board)
        layout.add_widget(self.info)
        self.game.current_player.find_valid_moves()
        
        self.board.draw_board()

        return layout
    """

class CheckersApp(App):
    def __init__(self, game):
        super().__init__()
        self.game = game
        
    """
    def build(self):
        self.start = GridLayout(cols = 1)
        startButton = Button(text= "Nová hra", font_size= 16)
        startButton.bind(on_press = self.start_game)
        self.start.add_widget(startButton)
        return self.start

    def start_game(self, instance):
        layout = BoxLayout(orientation="horizontal")
        self.info = InfoWidget(self.game)
        self.board = BoardWidget(self, cols=8, orientation="lr-bt")
        self.board.create_board()
        layout.add_widget(self.board)
        layout.add_widget(self.info)
        self.game.current_player.find_valid_moves()
        
        self.board.draw_board()

        return layout"""

    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        menu = MenuScreen(name = "Menu")
        game = GameScreen(self.game, name = "Checkers")
        game.board.squares
        sm.add_widget(menu)
        sm.add_widget(game)
        return sm
