from random import choice
from ConsoleGame import *
from HangmanStages import *
from Words import *
from string import ascii_uppercase

class HangmanGame(cdkkGame):
    def init(self):
        self.chosen_word = self.letters = self.guess = self.stage = self.allowed_words = None
        self.allowed_words = cdkkWords(word_length = self.get_config("letters", 6), common_words = True)
        return True

    def start(self):
        super().start()
        self.chosen_word = list(self.allowed_words.random_word())
        self.letters = []
        self.guess = list(" " * len(self.chosen_word))
        self.stage = 0

    def check(self, turn):
        turn_ok = turn in ascii_uppercase
        if turn_ok and turn in self.letters:
            turn_ok = False
        return turn_ok

    def update(self, turn):
        correct_guess = False
        for i, letter in enumerate(self.chosen_word):
            if letter == turn:
                self.guess[i] = letter
                correct_guess = True
        self.letters.append(turn)
        if not correct_guess:
            self.stage += 1

        # Update game status
        if (self.guess == self.chosen_word):
            # Player won
            self.status = self.current_player
        elif (self.stage == 7):
            self.status = 99  # Player lost

# ----------------------------------------

class HangmanPyPlayer(cdkkPyPlayer):
    def calculate_turn(self, game):
        # Randomly guess letters, checking that they haven't been used before
        answer = ''
        while answer == '':
            answer = choice(ascii_uppercase)
            if not game.check(answer):
                answer = ''

        return answer

# ----------------------------------------

class Hangman(cdkkConsoleGame):
    default_config = {
        "process_to_upper": True
    }

    def __init__(self, init_config=None):
        super().__init__(Hangman.default_config)
        self.update_config(init_config)
        self._console.set_config("silent", self.get_config("silent", False))
        self.game = HangmanGame(self.config)
        self.pyplayer = HangmanPyPlayer()
        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]HANGMAN[/blue] \n'
        self.instructions_str = "Guess one letter at a time."
        self.turn_pattern = "^[a-zA-Z]$"
        self.turn_pattern_error = "Please enter one letter.\n"
        self.check_turn_error = "You've used that letter already.\n"

    def display(self):
        self._console.print(hangman_stages[self.game.stage])
        display_guess = list(" " * len(self.game.guess) * 2)
        for i in range(len(self.game.guess)):
            if self.game.guess[i] == ' ':
                display_guess[i*2] = "_"
            else:
                display_guess[i*2] = self.game.guess[i]
        self._console.print(f"\n  [red]{''.join(display_guess)}[/red]\n")
        self._console.print(f"\n  Guesses so far: [blue]{' '.join(self.game.letters)}[/blue]\n")

    def end_game(self, outcome, num_players):
        if (outcome == 0 or outcome >= 99):
            self._console.print(f"Hard luck ... you lost. Correct Word: {''.join(self.game.chosen_word)}\n")
        else:
            if (num_players == 1):
                self._console.print(f"You beat Hangman in {len(self.game.letters)} guesses.\n")
            else:
                self._console.print(f"{self.players[outcome-1]} beat Hangman in {len(self.game.letters)} guesses.\n")

    def exit_game(self):
        self._console.print(self.games_wins_msg())

reg_game = Hangman()
reg_game.execute()

print("----------\n")

vs_game = Hangman({"players":2, "P2":"Python"})
vs_game.execute()

print("----------\n")

auto_game = Hangman({"letters":8, "P1":"Python", "silent":True, "auto_play_count": 1000})
auto_game.execute()
print(auto_game.games_wins_msg())

