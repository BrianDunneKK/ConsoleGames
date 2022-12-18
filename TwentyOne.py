from ConsoleGame import *
from cdkkGamePiece import Card, CardHand, CardDeck
from cdkkBoard import CardTable, CardPlayer, Board

# ----------------------------------------

class TwentyOneGame(Game):
    @property
    def player_score(self) -> int:
        return self.scores[0]

    @property
    def bank_score(self) -> int:
        return self.scores[1]

    def init(self) -> bool:
        super().init()
        self.table = CardTable(10,1)
        self.ready = {}
        self.deck = CardDeck()
        self.p1_context = {"style":"blue"}
        self.bank_context = {"hidden": True, "style":"red"}
        self.p1_player = CardPlayer(cards=CardHand(), table=self.table, deck=self.deck)
        self.bank_player = CardPlayer(cards=CardHand(), table=self.table, deck=self.deck, first_card=(9, 0), cards_dir=(-1, 0))
        return True

    def start(self) -> None:
        super().start()
        self.table.clear_all()
        self.deck.reset(shuffle=True)
        
        self.p1_player.clear()
        self.p1_player.deal(2, self.p1_context)
        self.p1_player.place_on_table()
        self.ready["P1"] = False

        self.bank_context["hidden"] = True
        self.bank_player.clear()
        self.bank_player.deal(2, context = self.bank_context)
        self.bank_player.place_on_table()
        self.ready["Bank"] = False
        self.next_after_update = False

    def total21(self, hand) -> int:
        total = 0
        for v in hand.values:
            total += min(v, 10)
        if (1 in hand.values) and total <= 11: # Ace scores 1 or 11
            total += 10
        return total

    def calc_scores(self) -> None:
        self.set_score(0, self.total21(self.p1_player))
        self.set_score(1, self.total21(self.bank_player))

    def update(self, turn) -> None:
        self.next_after_update = False
        self.calc_scores()

        if self.current_player == 1:
            if turn == 'T':
                self.p1_player.deal(1, self.p1_context)
            else:
                self.ready["P1"] = True
                self.bank_context["hidden"] = False    # Show bank's cards
                self.bank_player.add_context(self.bank_context)
                self.next_after_update = True
        else:
            if self.bank_score < self.player_score:
                self.bank_player.deal(1, self.bank_context)
            else:
                self.ready["Bank"] = True

        self.p1_player.place_on_table()
        self.bank_player.place_on_table()

    def update_status(self, turn) -> int:
        self.calc_scores()
        if (self.player_score > 21):
            self.status = 100                    # Player lost
        elif (self.bank_score > 21):
            self.status = 1                      # Player won
        elif self.ready["P1"] and self.bank_score > self.player_score: 
            self.status = 2                      # Player lost
        elif self.ready["Bank"] and self.player_score > self.bank_score: 
            self.status = 1                      # Player won
        elif self.ready["Bank"] and self.bank_score == self.player_score: 
            self.status = 0                      # Draw
        return self.status

# ----------------------------------------

class TwentyOneApp(cdkkConsoleGame):
    default_config = { "Game":{"players":2}, "ConsoleGame":{"P2":"Bank", "process_to_upper": True } }

    def __init__(self, init_config={}) -> None:
        super().__init__()
        self.game = TwentyOneGame()
        self.update_configs(cdkkConsoleGame.default_config, TwentyOneApp.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Twenty One[/blue] \n'
        self.instructions_str = "Enter T to Twist or S to Stick\n"
        self.turn_pattern = f"^[tsTS]|BANK$"
        self.turn_pattern_error = self.instructions_str

    def scores_str(self) -> str:
        return f"Player = {self.game.player_score},  Bank = {self.game.bank_score}"

    def display(self) -> None:
        super().display()
        self._console.print(f"\n [bold][blue]P l a y e r[/blue] [red]{'B a n k':>105}[/red][/bold]")
        self._console.print(*self.game.table.richtext(borders=Board.borders_sph2), sep="\n")

    def end_game(self, outcome, players) -> None:
        match outcome:
            case 0: msg = f"It was a draw ... {self.scores_str()}"
            case 1: msg = f"You won! ... {self.scores_str()}"
            case 100: msg = f"You're bust! ... Your score = {self.game.player_score}"
            case _: msg = f"You lost! ... {self.scores_str()}"
        self._console.print(f"\n{msg}\n")

    def exit_game(self) -> None:
        self._console.print(self.game_wins_msg())

twenty_one = TwentyOneApp()
twenty_one.execute()
