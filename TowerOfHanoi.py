import csv
from random import choice
from tkinter.tix import Tree
from ConsoleGame import *

class TowerOfHanoi(cdkkConsoleGame):
    styles = ["dark_orange3", "red", "yellow", "blue", "violet", "green"]

    def init(self):
        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Tower of Hanoi[/blue] \n'
        self.instructions_str = f"Move all disks to peg 3. Enter the source and destination peg numbers."
        self.turn_pattern = "^[1-3]{2}$"
        self.turn_pattern_error = "Please enter two digits.\n"

        self.disks = int(self.config.get_config("disks"))
        self.width = 4
        self.stack_width = 3 + self.disks * self.width
        self.pegs = [list(range(self.disks, 0, -1)), [], []]
        return True

    def start_game(self):
        super().start_game()
        self.pegs = [list(range(self.disks, 0, -1)), [], []]

    def process_turn(self):
        if super().process_turn():
            self.from_peg = int(self.next_turn[0]) -1
            self.to_peg = int(self.next_turn[1]) -1
            return True
        return False

    def check_turn(self):
        if (self.from_peg == self.to_peg):
            self._console.print(f"Please enter two different digits.\n")
            return False
        if len(self.pegs[self.from_peg]) == 0:
            self._console.print(f"There is no disk on peg {self.from_peg+1}\n")
            return False
        if len(self.pegs[self.to_peg]) > 0:
            if self.pegs[self.from_peg][-1] > self.pegs[self.to_peg][-1]:
                self._console.print(f"You can't move a disk between these pegs\n")
                return False
        return True

    def update(self):
        super().update()
        disk = self.pegs[self.from_peg].pop()
        self.pegs[self.to_peg].append(disk)

    def disk(self, size, block = '█'):
        # █ ▀ ▄ ▐ ▌
        width = min((size * self.width + 1), self.stack_width)
        str = (block * width).center(self.stack_width)
        return str

    def display(self):
        self._console.print('\n')
        for i in range(self.disks + 1):
            for j in range(3):
                peg = self.pegs[j]
                offset = self.disks - i
                if offset < len(peg):
                    size = peg[offset]
                else:
                    size = 0
                self._console.print(self.disk(size), style = TowerOfHanoi.styles[size], end = '')
            self._console.print('')

        for j in range(3):
            self._console.print(self.disk(99), style = TowerOfHanoi.styles[0], end = '')
        self._console.print('\n')

    def check_if_game_over(self):
        return(len(self.pegs[2]) == self.disks)

    def end_game(self):
        self._console.print(f"You beat Tower of Hanoi in {self.input_count} steps.\n")
        return True

hanoi = TowerOfHanoi({"disks":3})
hanoi.execute()
