from ConsoleGame import *
from cdkkBoard import Board
from TicTacToePyPlayer import *

class TicTacToeGame(Game):
    def init(self):
        self.players = 2
        super().init()
        self.board = Board(3,3, {0:".", 1:"X", 2:"O", -1:"?"})
        return True

    def start(self) -> None:
        super().start()
        self.board.clear_all()

    def check(self, turn: str) -> str:
        x, y, cmd = self.board.split_turn(turn)
        if x == -1:
            return "Please enter a valid square using the format 'col,row'"
        else:
            if self.board.get(x, y) != 0:
                return "Please enter a square using the format 'col,row'"
            else:
                return ""

    def update(self, turn) -> None:
        x, y, cmd = self.board.split_turn(turn)
        self.board.set(x, y, self.current_player)

    def update_status(self, turn) -> int:
        x, y, cmd = self.board.split_turn(turn)
        counts = self.board.in_a_row(x, y)
        if counts["max"] == 3:
            self.status = self.current_player    # Player won
        elif self.counts["turns"] == 9:
            self.status = 0    # Draw
        return self.status

# ----------------------------------------

class TicTacToe(cdkkConsoleGame):
    default_config = {}

    def __init__(self, init_config={}) -> None:
        super().__init__()
        self.game = TicTacToeGame()
        self.pyplayer = TicTacToePyPlayer()
        self.update_configs(cdkkConsoleGame.default_config, TicTacToe.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Tic Tac Toe[/blue] \n'
        self.instructions_str = "Select your square using the format 'row,col'."
        self.turn_pattern = "^[1-3],[1-3]$"
        self.turn_pattern_error = "Please enter a valid square.\n"

    def display(self) -> None:
        super().display()
        self._console.print("")
        ttt_borders = self.game.board.rt_stylise(Board.borders_all1, style="yellow")
        self._console.print(*self.game.board.richtext(borders=ttt_borders), sep="\n")
        self._console.print("")

    def end_game(self, outcome, players) -> None:
        if (outcome == 0 or outcome >= 99): 
            self._console.print(f"Draw game\n")
        else:
            self._console.print(f"{self.players[outcome-1]} won.\n")

    def exit_game(self) -> None:
        self._console.print(self.game_wins_msg())

ttt = TicTacToe()
#ttt.execute()

print("----------\n")

vs_game = TicTacToe({"ConsoleGame":{"P2":"Python"}})
vs_game.execute()
