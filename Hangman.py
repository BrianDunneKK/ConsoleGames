import csv
from random import choice
from ConsoleGame import *
from HangmanStages import *

class Hangman(cdkkConsoleGame):
    def init(self):
        # wordlist.txt contains the most common 5000 words
        with open("wordlist.txt") as f:
            all_words = f.read().splitlines()
        self._word_options = []
        for word in all_words:
            if (len(word) == self.get_config("letters")):
                self._word_options.append(word.upper())
        return True

    def start_game(self):
        self.console.clear()
        self.print(f'\n [red]WELCOME[/red] [green]TO[/green] [blue]HANGMAN[/blue] \n')
        self.print(f"You may start guessing letters.")
        self._chosen_word = list(choice(self._word_options).upper())
        self._letters = []
        self._guess = list(" " * len(self._chosen_word))
        self._stage = 0

    def process_input(self):
        self.user_input = self.user_input.upper()
        if len(self.user_input) != 1 or not self.user_input.isalpha():
            self.print(f"Please enter one letter.\n")
            return False
        elif self.user_input in self._letters:
            self.print(f"You've used that letter already.\n")
            return False
        else:
            return True

    def update(self):
        correct_guess = False
        for i, letter in enumerate(self._chosen_word):
            if letter == self.user_input:
                self._guess[i] = letter
                correct_guess = True
        self._letters.append(self.user_input)
        if not correct_guess:
            self._stage += 1

    def display(self, first_time = False):
        if not first_time:
            self.console.clear()
        self.print(hangman_stages[self._stage])
        display_guess = list(" " * len(self._guess) * 2)
        for i in range(len(self._guess)):
            if self._guess[i] == ' ':
                display_guess[i*2] = "_"
            else:
                display_guess[i*2] = self._guess[i]
        self.print(f"\n  [red]{''.join(display_guess)}[/red]\n")
        self.print(f"\n  Guesses so far: [blue]{' '.join(self._letters)}[/blue]\n")

    def check_if_game_over(self):
        return ((self._guess == self._chosen_word) or self._stage == 7)

    def end_game(self):
        if (self._guess == self._chosen_word):
            self.print(f"You beat Hangman in {len(self._letters)} guesses.\n")
        else:
            self.print(f"Hard luck ... you lost. Correct Word: {''.join(self._chosen_word)}\n")

game = Hangman({"letters":8})
game.execute()
