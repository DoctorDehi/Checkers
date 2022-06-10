from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.properties import OptionProperty, BooleanProperty

from enum import Enum
import time


from pieces import Man, King, Position
from pieces import Color as PieceColor


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
                         ellipse=(self.x + self.width // 3, self.y + self.height // 3, self.width//3, self.height//3),
                         width=1.5)

    def on_press(self):
        self.piece = "White"
        self.parent.game.player_white.add_piece(
            Man(PieceColor.WHITE, Position(self.row, self.column), self.parent.game.board)
        )
        self.parent.draw_board()

    def notation(self):
        return f"{'ABCDEFGH'[self.column]}{self.row + 1}"


class BoardWidget(GridLayout):
    squares = []

    def __init__(self, game, *args, **kwargs):
        super(BoardWidget, self).__init__(*args, **kwargs)
        self.game = game

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
                self.squares[row][column].canvas.ask_update()

    def on_touch_down(self, touch):
        moves = self.game.player_white.get_valid_moves()
        next_move = next(iter(moves.values()))[0]
        for position in self.game.make_move_gen(next_move):
            self.draw_board()
            self.parent.reset_context()


class InfoWidget(GridLayout):
    player = BooleanProperty(True)

    def __init__(self, game):
        super().__init__(cols=2)
        self.add_widget(Label(text="Current player: "))
        self.player_label = Label(text="White" if self.player else "Black")
        self.player = True
        self.add_widget(self.player_label)
        self.bind(player=self.player_changed)
        self.game = game

    def toggle_player(self):
        self.player = not self.player

    def player_changed(self, *args):
        self.player_label.text = "White" if self.player else "Black"
        self.player_label.color = (1, 1, 1) if self.player else (0.5, 0.5, 0.5)

    def on_touch_down(self, touch):
        self.toggle_player()


class CheckersApp(App):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.squares = []

    def build(self):
        layout = BoxLayout(orientation="horizontal")
        board = BoardWidget(self.game, cols=8, orientation="lr-bt")
        board.create_board()
        layout.add_widget(board)
        layout.add_widget(InfoWidget(self.game))

        board.draw_board()

        return layout


