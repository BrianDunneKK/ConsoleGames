from random import choice
from string import ascii_uppercase
from ConsoleGame import cdkkPyPlayer
from ConsoleGame import Game

class TowerOfHanoiPyPlayer(cdkkPyPlayer):
    def init(self, game: Game):
        self.turns = self.solve(game.disks, 1, 3)

    def calculate_turn(self, game: Game):
        return self.turns[game.counts["turns"]-1]

    def solve(self, count: int, from_peg: int, to_peg: int):
        from_to = f"{from_peg}{to_peg}"
        if count == 1:
            soln = [from_to]
        else:
            match from_to:
                case "23" | "32": third_peg = 1
                case "13" | "31": third_peg = 2
                case "12" | "21": third_peg = 3
            soln = self.solve(count-1, from_peg, third_peg)
            soln.append(from_to)
            soln.extend(self.solve(count-1, third_peg, to_peg))
        return soln


# ----------------------------------------

if __name__ == '__main__':
    pp = TowerOfHanoiPyPlayer()
    print(pp.solve(4, 1, 3))

