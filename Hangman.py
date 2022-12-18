from ConsoleGame import *
from cdkkWords import Words
from HangmanPyPlayer import *
from HangmanStages import *

class HangmanGame(Game):
    def init(self) -> bool:
        super().init()
        self.chosen_word = self.letters = self.guess = self.stage = self.allowed_words = None
        self.allowed_words = Words(word_length = self.config.get("letters", 6), common_words = True)
        return True

    def start(self) -> None:
        super().start()
        self.chosen_word = list(self.allowed_words.random_word())
        self.letters = []
        self.guess = list(" " * len(self.chosen_word))
        self.stage = 0

    def check(self, turn) -> str:
        turn_msg = "" if (turn in ascii_uppercase) else "Only upper case ASCII letters are allowed"
        if (turn_msg == "" and turn in self.letters):
            turn_msg = "You've used that letter already"
        return turn_msg

    def update(self, turn) -> None:
        correct_guess = False
        for i, letter in enumerate(self.chosen_word):
            if letter == turn:
                self.guess[i] = letter
                correct_guess = True
        self.letters.append(turn)
        if not correct_guess:
            self.stage += 1

    def update_status(self, turn) -> int:
        if (self.guess == self.chosen_word):
            self.status = self.current_player  # Player won
        elif (self.stage == 7):
            self.status = 99                   # Player lost
        return self.status

# ----------------------------------------

class Hangman(cdkkConsoleGame):
    default_config = { "ConsoleGame": { "process_to_upper": True } }

    def __init__(self, init_config={}) -> None:
        super().__init__()
        self.game = HangmanGame()
        self.pyplayer = HangmanPyPlayer()
        self.update_configs(cdkkConsoleGame.default_config, Hangman.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]HANGMAN[/blue] \n'
        self.instructions_str = "Guess one letter at a time."
        self.turn_pattern = "^[a-zA-Z]$"
        self.turn_pattern_error = "Please enter one letter.\n"

    def display(self) -> None:
        super().display()
        self._console.print(hangman_stages[self.game.stage])
        display_guess = list(" " * len(self.game.guess) * 2)
        for i in range(len(self.game.guess)):
            if self.game.guess[i] == ' ':
                display_guess[i*2] = "_"
            else:
                display_guess[i*2] = self.game.guess[i]
        self._console.print(f"\n  [red]{''.join(display_guess)}[/red]\n")
        self._console.print(f"\n  Guesses so far: [blue]{' '.join(self.game.letters)}[/blue]\n")

    def end_game(self, outcome, players) -> None:
        if (outcome == 0 or outcome >= 99):
            self._console.print(f"Hard luck ... you lost. Correct Word: {''.join(self.game.chosen_word)}\n")
        else:
            if (players == 1):
                self._console.print(f"You beat Hangman in {len(self.game.letters)} guesses.\n")
            else:
                self._console.print(f"{self.players[outcome-1]} beat Hangman in {len(self.game.letters)} guesses.\n")

    def exit_game(self) -> None:
        self._console.print(self.game_wins_msg())

reg_game = Hangman()
reg_game.execute()
print("----------\n")

vs_game = Hangman({"Game":{"players":2}, "ConsoleGame":{"P2":"Python"}})
#vs_game.execute()
#print("----------\n")

auto_cfg = {
    "Game":{"letters":8}
    ,"ConsoleGame":{"P1":"Python", "auto_play_count": 1000, "silent":True}
    ,"PyPlayer":{"pystrategy":"random"}
    } 
auto_random = Hangman(auto_cfg)
auto_random.execute()
print(auto_random.game_wins_msg())

freq_cfg = {
    "Game":{"letters":8}
    ,"ConsoleGame":{"P1":"Python", "auto_play_count": 100, "silent":True}
    ,"PyPlayer":{"pystrategy":"frequency"}
    } 
auto_freq = Hangman(freq_cfg)
auto_freq.execute()
print(auto_freq.game_wins_msg())
