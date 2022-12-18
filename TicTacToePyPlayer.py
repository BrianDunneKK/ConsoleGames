from random import choice
from ConsoleGame import cdkkPyPlayer
from ConsoleGame import Game

class TicTacToePyPlayer(cdkkPyPlayer):
    def calculate_turn(self, game: Game) -> str:
        options = []
        for y in range(game.board.ysize):
            for x in range(game.board.xsize):
                if game.board.get(x, y) == 0:
                    options.append((x,y))

        strategy = self.config.get("pystrategy", "random")
        if (strategy.upper() == "RANDOM"):
            return self.random(game, options)
        else:
            return("Unknown strategy")

    def random(self, game: Game, options: list[tuple[int,int]]) -> str:
        # Select a random square from those remaining
        x,y = choice(options)
        return (f"{x+1},{y+1}")

