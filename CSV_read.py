import csv
from pieces import Color, Man, King, Position
from Board import Board

class Hrač:
    def __init__(self, barva: Color):
        self.figurky = []
        self.barva = barva

    def nacti_figurku(self, b: Board):
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
                else:
                    print("Něco je špatně")
    
    def __repr__(self):
        return 

def main():
    b = Board(8)                
    hrac = Hrač(Color.BLACK)
    hrac.nacti_figurku(b)



if __name__ == "__main__":
    main()


