from ConsoleGame import *
from cdkkBoard import Board
from cdkkGamePiece import GamePiece, Dice

class YahtzeeBoard(Board):
    def create_piece(self, code: int = 0, value: int = -1) -> Dice:
        return Dice(code)

class YahtzeeGame(Game):
    def init(self) -> bool:
        super().init()
        self.board = YahtzeeBoard(5,1)
        return True

    def start(self) -> None:
        super().start()
        self.board.clear_all()
        for i in range(5):
            die = Dice(random_dice = True)
            self.board.set(i, 0, piece = die)

# ----------------------------------------

class Yahtzee(cdkkConsoleGame):
    default_config = {}

    def __init__(self, init_config={}) -> None:
        super().__init__()
        self.game = YahtzeeGame()
        self.update_configs(cdkkConsoleGame.default_config, Yahtzee.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Yahtzee[/blue] \n'
        self.instructions_str = "... Instructions go here ..."
        self.turn_pattern = "^[1-5]$"
        self.turn_pattern_error = "... Pattern error goes here ...\n"

    def display(self) -> None:
        super().display()
        self._console.print("")
        self._console.print(*self.game.board.richtext(borders=Board.borders_sph2), sep="\n")
        self._console.print("")

yahtzee = Yahtzee()
yahtzee.execute()
