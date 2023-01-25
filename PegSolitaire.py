from ConsoleGame import *
from cdkkBoard import *
from cdkkGamePiece import Counter3 

class Peg(Counter3):
    def __init__(self, code: int = 0):
        super().__init__(code = code, context = {"style":"blue"})

class PegSolitaireBoard(Board):
    def create_piece(self, code: int = 0, value: int = -1) -> Counter3:
        return Peg(code = code)


class PegSolitaireGame(Game):
    unused_mask = [
        [ 0,0,1,1,1,0,0]
        ,[0,0,1,1,1,0,0]
        ,[1,1,1,1,1,1,1]
        ,[1,1,1,1,1,1,1]
        ,[1,1,1,1,1,1,1]
        ,[0,0,1,1,1,0,0]
        ,[0,0,1,1,1,0,0]
    ]

    def init(self):
        super().init()
        self.board = PegSolitaireBoard(7, 7)
        self.board.set_unused_mask(PegSolitaireGame.unused_mask)
        return True

    def start(self) -> None:
        super().start()
        self.board.clear_all()
        self.board.fill(1)
        self.board.clear(self.board.xsize//2, self.board.ysize//2)

    def calc_options(self) -> list[str]:
        self.options.clear()
        pegs = self.board.filter_by_code(1)
        for x,y in pegs:
            gr = self.board.to_gridref(x, y).upper()
            for dir in list("NESW"):
                if  self.board.jump(x, y, dir, just_check=True) > 0:
                    self.options.append(gr + dir)
        return self.options

    def take(self, turn) -> None:
        x, y, dir = self.board.from_gridref(turn)
        self.board.jump(x, y, dir)

    def update_status(self, turn) -> int:
        if len(self.options) == 0:
            # Game over
            self.status = 2  # Assume player lost
            pegs = self.board.filter_by_code(1)
            if len(pegs) == 1:
                if pegs[0] == (self.board.xsize//2, self.board.ysize//2):
                    self.status = 1  # Player won
        return self.status

# ----------------------------------------

class PegSolitaire(cdkkConsoleGame):
    default_config = { "ConsoleGame": { "process_to_upper": True, "process_xydir_map": True } }

    def __init__(self, init_config={}) -> None:
        super().__init__()
        self.game = PegSolitaireGame()
        self.update_configs(cdkkConsoleGame.default_config, PegSolitaire.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Solitaire[/blue] \n'
        self.instructions_str = "Enter the grid referene and the jump direction."
        self.turn_pattern = "^[A-G][1-7][UDLRNESW]$"
        self.turn_pattern_error = "Please enter a valid grid reference and jump direction.\n"

    def display(self) -> None:
        super().display()
        self._console.print("")
        ttt_borders = self.game.board.rt_stylise(Board.borders_single1, style="yellow")
        self._console.print(*self.game.board.richtext(borders=ttt_borders, unused = Text('█', style = "yellow"), gridref = "yellow"), sep="\n")
        self._console.print("")

    def exit_game(self) -> None:
        self._console.print(self.game_wins_msg())

ttt = PegSolitaire()
ttt.execute()
