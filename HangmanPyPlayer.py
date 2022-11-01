from random import choice
from string import ascii_uppercase
from ConsoleGame import cdkkPyPlayer
from ConsoleGame import Game

class HangmanPyPlayer(cdkkPyPlayer):
    def init(self, game: Game):
        self.freq = game.allowed_words.frequency()

    def calculate_turn(self, game: Game):
        strategy = self.config.get("pystrategy", "random")
        if (strategy.upper() == "RANDOM"):
            return self.random(game)
        elif (strategy.upper() == "FREQUENCY"):
            return self.frequency(game)
        else:
            return("Unknown strategy")

    def random(self, game: Game):
        # Randomly guess letters, checking that they haven't been used before
        answer = ''
        while answer == '':
            answer = choice(ascii_uppercase)
            if game.check(answer) != "":
                answer = ''

        return answer

    def frequency(self, game: Game):
        # Frequency analysis
        freq = [letter for letter in self.freq if not (letter in game.letters)]
        return freq[0]
