import csv
from random import choice
from ConsoleGame import *

class TowerOfHanoiGame(cdkkGame):
    def init(self):
        self.disks = int(self.get_config("disks"))
        self.pegs = [list(range(self.disks, 0, -1)), [], []]
        return True

    def start(self):
        super().start()
        self.pegs = [list(range(self.disks, 0, -1)), [], []]

    def check(self, turn):
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

    def update(self, turn):
        disk = self.pegs[int(turn[0]) - 1].pop()
        self.pegs[int(turn[1]) - 1].append(disk)

        # Update game status
        if (len(self.pegs[2]) == self.disks):
            # Game over
            self.status = self.current_player

# ----------------------------------------

class TowerOfHanoi(cdkkConsoleGame):
    default_config = {}
    styles = ["dark_orange3", "red", "yellow", "blue", "violet", "green"]

    def __init__(self, init_config=None):
        super().__init__(TowerOfHanoi.default_config)
        self.update_config(init_config)
        self._console.set_config("silent", self.get_config("silent", False))
        self.game = TowerOfHanoiGame(self.config)
        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Tower of Hanoi[/blue] \n'
        self.instructions_str = f"Move all disks to peg 3. Enter the source and destination peg numbers."
        self.turn_pattern = "^[1-3]{2}$"
        self.turn_pattern_error = "Please enter two digits.\n"
        self.check_turn_error = "Invalid combination: "

    def disk(self, size, block = '█'):
        # █ ▀ ▄ ▐ ▌
        width_multiplier = 4
        stack_width = 3 + self.game.disks * width_multiplier
        width = min((size * width_multiplier + 1), stack_width)
        str = (block * width).center(stack_width)
        return str

    def display(self):
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

    def end_game(self, outcome, num_players):
        self._console.print(f"You beat Tower of Hanoi in {self.game.turn_count} steps.\n")

hanoi = TowerOfHanoi({"disks":3})
hanoi.execute()
