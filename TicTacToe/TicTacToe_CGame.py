from TicTacToe import *
from cdkkConsoleGame import cdkkConsoleGame

class TicTacToe(cdkkConsoleGame):
    default_config = { "ConsoleGame": { "process_to_upper": True } }

    def __init__(self, init_config={}) -> None:
        super().__init__()
        self.game = TicTacToeGame()
        self.pyplayer = TicTacToePyPlayer()
        self.update_configs(cdkkConsoleGame.default_config, TicTacToe.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Tic Tac Toe[/blue] \n'
        self.instructions_str = "Select your square using a grid reference (for example 'a1')."
        self.turn_pattern = "^[A-C][1-3]$"
        self.turn_pattern_error = "Please enter a valid grid reference.\n"

    def display(self) -> None:
        super().display()
        self._console.print("")
        ttt_borders = self.game.board.rt_stylise(Board.borders_single2, style="yellow")
        self._console.print(*self.game.board.richtext(borders=ttt_borders, gridref = "bright_black"), sep="\n")
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
