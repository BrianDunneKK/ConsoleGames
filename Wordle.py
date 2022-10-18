import csv
from random import choice
from ConsoleGame import *
from Words import *

class Wordle(cdkkConsoleGame):
    def init(self):
        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]WORDLE[/blue] \n'
        self.instructions_str = f"Guess words with {self.get_config('letters')} letters."
        self.input_pattern = f"^[a-zA-Z]{{{self.get_config('letters')}}}$"
        self.input_error = f"Please enter a valid {self.get_config('letters')}-letter word.\n"
        self._common_words = cdkkWords(word_length = self.get_config("letters"), common_words = True)
        self._all_words = cdkkWords(word_length = self.get_config("letters"), common_words = False)
        return True

    def start_game(self):
        super().start_game()
        self._chosen_word = self._common_words.random_word()
        # self._chosen_word = choice(self._word_options)
        self._guesses = []
        self._guesses_coloured = []

    def process_input(self):
        self.user_input = self.user_input.upper()
        return super().process_input()

    def valid_input(self):
        if self._all_words.contains_word(self.user_input):
            return True
        self.print(f"Please enter a valid word!!\n")
        return False

    def update(self):
        super().update()
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
            return True
        else:
            self.print(f"Hard luck ... you used all {self.get_config('guesses')} guesses. Correct Word: {self._chosen_word}\n")
            return False

game = Wordle({"letters":5, "guesses":6, "players":1})
game.execute()
