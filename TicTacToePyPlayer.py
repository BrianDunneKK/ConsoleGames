from random import choice
from ConsoleGame import cdkkPyPlayer
from ConsoleGame import Game

class TicTacToePyPlayer(cdkkPyPlayer):
    def calculate_turn(self, game: Game) -> str:
        strategy = str(self.config.get("pystrategy", "random"))
        if (strategy.upper() == "RANDOM"):
            return self.random(game, game.options)
        else:
            return("Unknown strategy")

    def random(self, game: Game, options: list[str]) -> str:
        # Select a random square from those remaining
        return choice(options)

