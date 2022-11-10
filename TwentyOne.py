# To Do: Change "code + 100" to hidden context

from ConsoleGame import *
from cdkkBoard import Board
from cdkkGamePiece import GamePiece, GamePieceSet, Card

class CardTwentyOne(Card):
    @property
    def value(self):
        return min(self._value, 10)

# ----------------------------------------

class HandTwentyOne(GamePieceSet):
    @property
    def total(self):
        total0 = sum(self.values)
        return total0

# ----------------------------------------

class BoardTwentyOne(Board):
    def create_piece(self, code: int = 0, value: int = -1):
        return CardTwentyOne(code)

# ----------------------------------------

class TwentyOneGame(Game):
    def init(self):
        super().init()
        self.board = BoardTwentyOne(10,1)
        return True

    def start(self):
        super().start()
        self.board.clear_all()
        self.twist("P1")
        self.twist("P1")
        self.twist("Bank", 100, from_left = False)
        self.twist("Bank", 100, from_left = False)
        self.next_after_update = False

    def twist(self, player: str, code_inc: int = 0, from_left: bool = True):
        hand = HandTwentyOne(self.board.filter_pieces({"player":player}))
        card = CardTwentyOne(random_card = True, context = {"player":player})
        card.set(code_inc + card.code)
        offset = hand.count if from_left else (self.board.xsize - hand.count - 1)
        self.board.set(offset, 0, piece = card)

    def update(self, turn):
        self.next_after_update = False
        if self.current_player == 1:
            if turn == 'T':
                self.twist("P1")
                hand = HandTwentyOne(self.board.filter_pieces({"player":"P1"}))
                print(f"Total = {hand.total}")
            else:
                card = self.board.get_piece(9, 0)
                card.set(card.code - 100)
                card = self.board.get_piece(8, 0)
                card.set(card.code - 100)
                self.next_after_update = True
        else:
            self.twist("Bank", from_left = False)

        # Update game status
        hand = HandTwentyOne(self.board.filter_pieces({"player":"P1"}))
        if (hand.total > 21):
            self.status = 99                     # Player lost
        elif self.counts["turns"] > 7:
            self.status = self.current_player    # Player won

# ----------------------------------------

class TwentyOne(cdkkConsoleGame):
    default_config = { "Game":{"players":2}, "ConsoleGame":{"P2":"Bank", "process_to_upper": True } }

    def __init__(self, init_config={}):
        super().__init__()
        self.game = TwentyOneGame()
        self.update_configs(cdkkConsoleGame.default_config, TwentyOne.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Twenty One[/blue] \n'
        self.instructions_str = "Enter T to Twist or S to Stick"
        self.turn_pattern = f"^[tsTS]|BANK$"
        self.turn_pattern_error = "... Pattern error goes here ...\n"

    def display(self):
        super().display()
        self._console.print(f"\n [bold][blue]P l a y e r[/blue] [red]{'B a n k':>105}[/red][/bold]")
        self._console.print(*self.game.board.strings(), sep="\n")
        self._console.print("")

    def end_game(self, outcome, players):
        if (outcome == 0 or outcome >= 99):
            self._console.print(f"Hard luck ... you lost.\n")

TwentyOne = TwentyOne()
TwentyOne.execute()
