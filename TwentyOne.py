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
        total = sum(self.values)
        if (1 in self.values) and total <= 11:
            total += 10
        return total
        
# ----------------------------------------

class BoardTwentyOne(Board):
    def create_piece(self, code: int = 0, value: int = -1):
        return CardTwentyOne(code)

# ----------------------------------------

class TwentyOneGame(Game):
    def init(self):
        super().init()
        self.board = BoardTwentyOne(10,1)
        self.scores = {}
        self.ready = {}
        return True

    def start(self):
        super().start()
        self.board.clear_all()
        self.twist("P1")
        self.twist("P1")
        self.twist("Bank", hidden = True, from_left = False)
        self.twist("Bank", hidden = True, from_left = False)
        self.calc_scores()
        self.ready["P1"] = False
        self.ready["Bank"] = False
        self.next_after_update = False

    def calc_scores(self) -> None:
        p1_hand = HandTwentyOne(self.board.filter_pieces({"player":"P1"}))
        bank_hand = HandTwentyOne(self.board.filter_pieces({"player":"Bank"}))
        self.scores["P1"] = p1_hand.total
        self.scores["Bank"] = bank_hand.total

    def twist(self, player: str, hidden: bool = False, from_left: bool = True):
        hand = HandTwentyOne(self.board.filter_pieces({"player":player}))
        card = CardTwentyOne(random_card = True, context = {"player":player})
        card.set(card.code, context = {"hidden": hidden})
        offset = hand.count if from_left else (self.board.xsize - hand.count - 1)
        self.board.set(offset, 0, piece = card)

    def update(self, turn):
        self.next_after_update = False
        self.calc_scores()

        if self.current_player == 1:
            if turn == 'T':
                self.twist("P1")
            else:
                self.ready["P1"] = True
                card = self.board.get_piece(9, 0)
                card.context["hidden"] = False
                card = self.board.get_piece(8, 0)
                card.context["hidden"] = False
                self.next_after_update = True
        else:
            if self.scores["Bank"] < self.scores["P1"] or self.scores["Bank"] <= 14:
                self.twist("Bank", from_left = False)
            else:
                self.ready["Bank"] = True

        # Update game status
        self.calc_scores()
        if (self.scores["P1"] > 21):
            self.status = 100                    # Player lost
        elif (self.scores["Bank"] > 21):
            self.status = 1                      # Player won
        elif self.ready["P1"] and self.scores["Bank"] > self.scores["P1"]: 
            self.status = 99                     # Player lost
        elif self.ready["Bank"] and self.scores["P1"] > self.scores["Bank"]: 
            self.status = 1                      # Player won
        elif self.ready["Bank"] and self.scores["Bank"] == self.scores["P1"]: 
            self.status = 0                      # Draw

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

    def scores_str(self):
        return f"Player = {self.game.scores['P1']},  Bank = {self.game.scores['Bank']}"

    def display(self):
        super().display()
        self._console.print(f"\n [bold][blue]P l a y e r[/blue] [red]{'B a n k':>105}[/red][/bold]")
        self._console.print(*self.game.board.strings(), sep="\n")

    def end_game(self, outcome, players):
        match outcome:
            case 0: msg = f"It was a draw ... {self.scores_str()}"
            case 1: msg = f"You won! ... {self.scores_str()}"
            case 100: msg = f"You're bust! ... Your score = {self.game.scores['P1']}"
            case _: msg = f"You lost! ... {self.scores_str()}"
        self._console.print(f"\n{msg}\n")

    def exit_game(self):
        self._console.print(self.game_wins_msg())

TwentyOne = TwentyOne()
TwentyOne.execute()
