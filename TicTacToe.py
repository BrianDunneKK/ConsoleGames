from ConsoleGame import *
from cdkkBoard import Board

class TicTacToeGame(Game):
    def init(self):
        self.players = 2
        super().init()
        self.board = Board(3,3, {0:".", 1:"X", 2:"O", -1:"?"})
        return True

    def start(self):
        super().start()
        self.board.clear_all()

    def check(self, turn: str):
        x, y, cmd = self.board.split_turn(turn)
        if x == -1:
            return "Please enter a valid square using the format 'col,row'"
        else:
            if self.board.get(x, y) != 0:
                return "Please enter a square using the format 'col,row'"
            else:
                return ""

    def update(self, turn):
        x, y, cmd = self.board.split_turn(turn)
        self.board.set(x, y, self.current_player)

        # Update game status
        counts = self.board.in_a_row(x, y)
        if counts["max"] == 3:
            self.status = self.current_player    # Player won
        elif self.counts["turns"] == 9:
            self.status = 0    # Draw

# ----------------------------------------

class TicTacToe(cdkkConsoleGame):
    default_config = {}

    def __init__(self, init_config={}):
        super().__init__()
        self.game = TicTacToeGame()
        self.update_configs(cdkkConsoleGame.default_config, TicTacToe.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Tic Tac Toe[/blue] \n'
        self.instructions_str = "Select your square using the format 'row,col'."
        self.turn_pattern = "^[1-3],[1-3]$"
        self.turn_pattern_error = "Please enter a valid square.\n"

    def display(self):
        super().display()
        self._console.print("")
        self._console.print(*self.game.board.strings(), sep="\n")
        self._console.print("")

    def end_game(self, outcome, players):
        if (outcome == 0 or outcome >= 99):
            self._console.print(f"Draw game\n")
        else:
            self._console.print(f"{self.players[outcome-1]} won.\n")

    def exit_game(self):
        self._console.print(self.game_wins_msg())

TicTacToe = TicTacToe()
TicTacToe.execute()
