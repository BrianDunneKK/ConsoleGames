import csv
from random import choice
from ConsoleGame import *
from Words import *

class WordleGame(cdkkGame):
    def init(self):
        self.common_words = cdkkWords(word_length = self.get_config("letters", 6), common_words = True)
        self.allowed_words = cdkkWords(word_length = self.get_config("letters", 6), common_words = False)
        return True

    def start(self):
        super().start()
        self.chosen_word = self.common_words.random_word()
        self.guesses = []
        self.guesses_coloured = []

    def check(self, turn):
        return self.allowed_words.contains_word(turn)

    def update(self, turn):
        coloured = ""
        for i, letter in enumerate(turn):
            if letter == self.chosen_word[i]:
                colour = "green"
            elif letter in self.chosen_word:
                colour = "yellow"
            else:
                colour = "default"
            coloured += f"[{colour}]{letter}[/{colour}] "
        self.guesses.append(turn)
        self.guesses_coloured.append(coloured)

        # Update game status
        if (turn == self.chosen_word):
            # Player won
            self.status = self.current_player
        elif (len(self.guesses) == self.get_config('guesses')):
            # Player lost
            self.status = 99

# ----------------------------------------

class Wordle(cdkkConsoleGame):
    default_config = {
        "process_to_upper": True
    }

    def __init__(self, init_config=None):
        super().__init__(Wordle.default_config)
        self.update_config(init_config)
        self._console.set_config("silent", self.get_config("silent", False))
        self.game = WordleGame(self.config)
        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]WORDLE[/blue] \n'
        self.instructions_str = f"Guess words with {self.get_config('letters')} letters."
        self.turn_pattern = f"^[a-zA-Z]{{{self.get_config('letters')}}}$"
        self.turn_pattern_error = f"Please enter a valid {self.get_config('letters')}-letter word.\n"
        self.check_turn_error = "Please enter a valid word.\n"

    def display(self):
        self._console.print(*self.game.guesses_coloured, sep="\n")
        self._console.print("")

    def end_game(self, outcome, num_players):
        if (outcome == 0 or outcome >= 99):
            self._console.print(f"Hard luck ... you used all {self.get_config('guesses')} guesses. Correct Word: {self.game.chosen_word}\n")
        else:
            if (num_players == 1):
                self._console.print(f"You beat WORDLE in {len(self.game.guesses)}/{self.get_config('guesses')} guesses.\n")
            else:
                self._console.print(f"{self.players[outcome-1]} beat WORDLE in {self.game.turn_count} guesses.\n")

    def exit_game(self):
        self._console.print(self.games_wins_msg())

wordle = Wordle({"letters":5, "guesses":6, "players":2})
wordle.execute()
