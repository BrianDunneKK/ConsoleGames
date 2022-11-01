from random import choice
from string import ascii_uppercase
from ConsoleGame import cdkkPyPlayer
from ConsoleGame import Game

class TowerOfHanoiPyPlayer(cdkkPyPlayer):
    def init(self, game: Game):
        # To Do: Calculate turns for more than 3 disks
        self.turns = ["13", "12", "32", "13", "21", "23", "13"]

    def calculate_turn(self, game: Game):
        return self.turns[game.counts["turns"]-1]

    def random(self, game):
        # Randomly guess letters, checking that they haven't been used before
        answer = ''
        while answer == '':
            answer = choice(ascii_uppercase)
            if game.check(answer) != "":
                answer = ''

        return answer

    def frequency(self, game: Game):
        # Frequency analysis
        freq = game.allowed_words.frequency()
        freq = [letter for letter in freq if not (letter in game.letters)]
        return freq[0]
