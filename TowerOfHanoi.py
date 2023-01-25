from ConsoleGame import *
from TowerOfHanoiPyPlayer import TowerOfHanoiPyPlayer

class TowerOfHanoiGame(Game):
    def init(self) -> bool:
        super().init()
        self.disks = int(self.config.get("disks"))
        self.pegs = [list(range(self.disks, 0, -1)), [], []]
        return True

    def start(self) -> None:
        super().start()
        self.pegs = [list(range(self.disks, 0, -1)), [], []]

    def check(self, turn) -> str:
        from_peg = int(turn[0]) - 1
        to_peg = int(turn[1]) - 1
        if (from_peg == to_peg):
            return ("Please enter two different digits")
        if len(self.pegs[from_peg]) == 0:
            return (f"There is no disk on peg {from_peg+1}")
        if len(self.pegs[to_peg]) > 0:
            if self.pegs[from_peg][-1] > self.pegs[to_peg][-1]:
                return ("You can't move a disk between these pegs")
        return ""

    def take(self, turn) -> None:
        disk = self.pegs[int(turn[0]) - 1].pop()
        self.pegs[int(turn[1]) - 1].append(disk)

    def update_status(self, turn) -> int:
        if (len(self.pegs[2]) == self.disks):
            self.status = self.current_player   # Game over
        return self.status

# ----------------------------------------

class TowerOfHanoi(cdkkConsoleGame):
    default_config = {}
    styles = ["dark_orange3", "red", "yellow", "blue", "violet", "green"]

    def __init__(self, init_config={}) -> None:
        super().__init__()
        self.game = TowerOfHanoiGame()
        self.pyplayer = TowerOfHanoiPyPlayer()
        self.update_configs(cdkkConsoleGame.default_config, TowerOfHanoi.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Tower of Hanoi[/blue] \n'
        self.instructions_str = f"Move all disks to peg 3. Enter the source and destination peg numbers."
        self.turn_pattern = "^[1-3]{2}$"
        self.turn_pattern_error = "Please enter two digits.\n"
        self.check_turn_error = "Invalid combination: "

    def disk(self, size, block = '█') -> str:        # █ ▀ ▄ ▐ ▌
        width_multiplier = 4
        stack_width = 3 + self.game.disks * width_multiplier
        width = min((size * width_multiplier + 1), stack_width)
        str = (block * width).center(stack_width)
        return str

    def display(self) -> None:
        super().display()
        self._console.print('\n')
        for i in range(self.game.disks + 1):
            for j in range(3):
                peg = self.game.pegs[j]
                offset = self.game.disks - i
                if offset < len(peg):
                    size = peg[offset]
                else:
                    size = 0
                self._console.print(self.disk(size), style = TowerOfHanoi.styles[size], end = '')
            self._console.print('')

        for j in range(3):
            self._console.print(self.disk(99), style = TowerOfHanoi.styles[0], end = '')
        self._console.print('\n')

    def end_game(self, outcome, players) -> None:
        self._console.print(f"You beat Tower of Hanoi in {self.game.counts['turns']} steps.\n")

# ----------------------------------------

hanoi = TowerOfHanoi({"Game":{"disks":3}})
hanoi.execute()

hanoi_cfg = {
    "Game": {"disks":5}
    ,"ConsoleGame": {"P1":"Python", "python_sleep":0.5, "exit_at_end": True, "cls_pre_display": True}
    }
hanoi_auto = TowerOfHanoi(hanoi_cfg)
hanoi_auto.execute()
