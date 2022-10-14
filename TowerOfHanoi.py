import csv
from random import choice
from ConsoleGame import *

class TowerOfHanoi(cdkkConsoleGame):
    styles = ["dark_orange3", "red", "yellow", "blue", "violet", "green"]

    def init(self):
        self.disks = int(self.get_config("disks"))
        self.width = 4
        self.stack_width = 3 + self.disks * self.width
        self.pegs = [list(range(self.disks, 0, -1)), [], []]
        return True

    def start_game(self):
        self.print(f'\n [red]WELCOME[/red] [green]TO[/green] [blue]Tower of Hanoi[/blue] \n')

    def process_input(self):
        if len(self.user_input) != 2:
            self.print(f"Please enter two digits\n")
            return False
        if not (self.user_input[0].isnumeric() and self.user_input[1].isnumeric()):
            self.print(f"Please enter two digits\n")
            return False
        self.from_peg = int(self.user_input[0]) -1
        self.to_peg = int(self.user_input[1]) -1
        if (self.from_peg < 0 or self.from_peg > 2 or self.to_peg < 0 or self.to_peg > 2 or self.from_peg == self.to_peg):
            self.print(f"Please enter two different digits, each between 1 and 3\n")
            return False
        if len(self.pegs[self.from_peg]) == 0:
            self.print(f"There is no disk on peg {self.from_peg+1}\n")
            return False
        if len(self.pegs[self.to_peg]) > 0:
            if self.pegs[self.from_peg][-1] > self.pegs[self.to_peg][-1]:
                self.print(f"You can't move a disk between these pegs\n")
                return False
        return True

    def update(self):
        disk = self.pegs[self.from_peg].pop()
        self.pegs[self.to_peg].append(disk)

    def disk(self, size, block = '█'):
        # █ ▀ ▄ ▐ ▌
        width = min((size * self.width + 1), self.stack_width)
        str = (block * width).center(self.stack_width)
        return str

    def display(self, first_time = False):
        if not first_time:
            self.console.clear()
        self.print('\n')
        for i in range(self.disks + 1):
            for j in range(3):
                peg = self.pegs[j]
                offset = self.disks - i
                if offset < len(peg):
                    size = peg[offset]
                else:
                    size = 0
                self.print(self.disk(size), style = TowerOfHanoi.styles[size], end = '')
            self.print('')

        for j in range(3):
            self.print(self.disk(99), style = TowerOfHanoi.styles[0], end = '')
        self.print('\n')

    def check_if_game_over(self):
        return(len(self.pegs[2]) == self.disks)

    def end_game(self):
        self.print(f"You beat Tower of Hanoi\n")

game = TowerOfHanoi({"disks":3})
game.execute()
