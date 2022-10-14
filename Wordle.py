import csv
from random import choice
from ConsoleGame import *

class Wordle(cdkkConsoleGame):
    def init(self):
        self.input_pattern = f"^[a-zA-Z]{{{self.get_config('letters')}}}$"
        self.input_error = f"Please enter a valid {self.get_config('letters')}-letter word.\n"

        # wordlist.txt contains the most common 5000 words
        # The chosen word comes from ths list
        with open("wordlist.txt") as f:
            all_words = f.read().splitlines()
        self._word_options = []
        for word in all_words:
            if (len(word) == self.get_config("letters")):
                self._word_options.append(word.upper())

        # wordlist#.txt contains all words with # letters (#=3-9)
        # Users can enter any word on this list
        with open(f"wordlist{self.get_config('letters')}.txt") as f:
            all_words = f.read().splitlines()
        self._allowed_words = []
        for word in all_words:
            self._allowed_words.append(word.upper())

        return True

    def start_game(self):
        self.print(f'\n [red]WELCOME[/red] [green]TO[/green] [blue]WORDLE[/blue] \n')
        self.print(f"You may start guessing words with {self.get_config('letters')} letters.")
        self._chosen_word = choice(self._word_options)
        self._guesses = []
        self._guesses_coloured = []

    def process_input(self):
        self.user_input = self.user_input.upper()
        return super().process_input()

    def valid_input(self):
        if (self.user_input not in self._allowed_words):
            self.print(f"Please enter a valid word!!\n")
            return False
        else:
            return True

    def update(self):
        coloured = ""
        for i, letter in enumerate(self.user_input):
            if self._chosen_word[i] == self.user_input[i]:
                colour = "green"
            elif letter in self._chosen_word:
                colour = "yellow"
            else:
                colour = "default"
            coloured += f"[{colour}]{letter}[/{colour}] "
        self._guesses.append(self.user_input)
        self._guesses_coloured.append(coloured)

    def display(self, first_time = False):
        self.print(*self._guesses_coloured, sep="\n")
        self.print("")

    def check_if_game_over(self):
        return (self.user_input == self._chosen_word) or (len(self._guesses) == self.get_config('guesses'))

    def end_game(self):
        if (self.user_input == self._chosen_word):
            self.print(f"You beat WORDLE {len(self._guesses)}/{self.get_config('guesses')}\n")
        else:
            self.print(f"Hard luck ... you used all {self.get_config('guesses')} guesses. Correct Word: {self._chosen_word}\n")

game = Wordle({"letters":5, "guesses":6})
game.execute()
