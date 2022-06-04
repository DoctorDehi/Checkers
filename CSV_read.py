import csv
from pieces import Color, Man, King, Position
from Board import Board

class Hrač:
    def __init__(self, barva: Color):
        self.figurky = []
        self.barva = barva

    def nacti_figurku(self, b: Board):
        try:
            with open('nacti.csv', 'r') as soubor:
                reader = csv.reader(soubor)
                for row in reader:
                    if row[1] == "b" and self.barva == Color.BLACK:
                        self.figurky.append(Man(Color.BLACK, Position.from_notation(row[0]), b))
                    elif row[1] == "bb" and self.barva == Color.BLACK:
                        self.figurky.append(King(Color.BLACK, Position.from_notation(row[0]), b))
                    elif row[1] == "w" and self.barva == Color.WHITE:
                        self.figurky.append(Man(Color.WHITE, Position.from_notation(row[0]), b))
                    elif row[1] == "ww" and self.barva == Color.WHITE:
                        self.figurky.append(King(Color.WHITE, Position.from_notation(row[0]), b))
        except:
            raise Exception("V načítání se vyskytla chyba")
    
    def __repr__(self):
        return self.figurky



