
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.win = 0

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    def radoms(self):
        quit = random.randint(1, 6)
        return quit
    def play_round(self):
        self.sum1 = 0
        self.sum2 = 0
        for i in range(2):
            self.sum1 += game.radoms()
            self.sum2 += game.radoms()
        print(f'{player1.name} выбросил {self.sum1}')
        print(f'{player2.name} выбросил {self.sum2}')
        if self.sum1 > self.sum2:
            print(f'Победил {player1.name}\n')
            self.player1.win += 1
        elif self.sum1 < self.sum2:
            print(f'Победил {player2.name}\n')
            self.player2.win += 1
        else:
            print('Ничья')
    def statis(self):
        print(f'{player1.name} Побед {player1.win}')
        print(f'{player2.name} Побед {player2.win}')
player1 = Player("Alice")
player2 = Player("Bob")
game = Game(player1, player2)
game.play_round()
game.play_round()
game.statis()
