import sys
import os
github_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cdkk'))
sys.path.append(github_path)

from random import choice
from cdkkBoard import Board
from cdkkConsoleGame import (Game, cdkkPyPlayer)

# ----------------------------------------

class TicTacToeGame(Game):
    def init(self):
        self.players = 2
        super().init()
        self.board = Board(3,3, {0:".", 1:"X", 2:"O", -1:"?"})
        return True

    def start(self) -> None:
        super().start()
        self.board.clear_all()

    def calc_options(self) -> list[str]:
        self.options.clear()
        blanks = self.board.filter_by_code(0)
        for x,y in blanks:
            self.options.append(self.board.to_gridref(x, y).upper())
        return self.options

    def take(self, turn) -> None:
        x, y, cmd = self.board.from_gridref(turn)
        self.board.set(x, y, self.current_player)

    def update_status(self, turn) -> int:
        x, y, cmd = self.board.from_gridref(turn)
        counts = self.board.in_a_row(x, y)
        if counts["max"] == 3:
            self.status = self.current_player   # Player won
        elif self.counts["turns"] == 9:
            self.status = 0                     # Draw
        return self.status

# ----------------------------------------

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

