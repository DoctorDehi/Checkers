from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import OptionProperty, BooleanProperty

from enum import Enum


class SquareColor(Enum):
    BLACK = 0
    LIGHT = 1


class Square(Button):
    piece = OptionProperty("None", options=["None", "White", "Black", "WhiteK", "BLackK"])

    def __init__(self, i):
        self.line = 7 - i // 8
        self.col = i % 8
        self.scolor = SquareColor.BLACK if (self.line + self.col) % 2 == 0 else SquareColor.LIGHT
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

            if self.piece in ["Black", "BlackK"]:
                Color(0, 0, 0)
            else:
                Color(1, 1, 1)

            if self.piece != "None":
                Ellipse(pos=(self.x + self.width // 6, self.y + self.height // 6),
                        size=(2 * self.width // 3, 2 * self.height // 3))

    def on_press(self):
        self.piece = "White"

    def notation(self):
        return f"{'ABCDEFGH'[self.col]}{self.line + 1}"


class InfoWidget(GridLayout):
    player = BooleanProperty(True)

    def __init__(self):
        super().__init__(cols=2)
        self.add_widget(Label(text="Current player: "))
        self.player_label = Label(text="White" if self.player else "Black")
        self.player = True
        self.add_widget(self.player_label)
        self.bind(player=self.player_changed)

    def toggle_player(self):
        self.player = not self.player

    def player_changed(self, *args):
        self.player_label.text = "White" if self.player else "Black"
        self.player_label.color = (1, 1, 1) if self.player else (0.5, 0.5, 0.5)

    def on_touch_down(self, touch):
        self.toggle_player()


class CheckersApp(App):
    def build(self):
        layout = BoxLayout(orientation="horizontal")

        ilayout = GridLayout(cols=8)

        for i in range(64):
            ilayout.add_widget(Square(i))

        layout.add_widget(ilayout)
        layout.add_widget(InfoWidget())

        return layout
