import csv
from random import choice
from ConsoleGame import *
from HangmanStages import *
from Words import *
from string import ascii_uppercase

class Hangman(cdkkConsoleGame):
    def init(self):
        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]HANGMAN[/blue] \n'
        self.instructions_str = "Guess one letter at a time."
        self.input_pattern = "^[a-zA-Z]$"
        self.input_error = "Please enter one letter.\n"
        self._words = cdkkWords(word_length = self.get_config("letters"), common_words = True)
        return True

    def read_game_config(self):
        super().read_game_config()

    def start_game(self):
        super().start_game()
        self._chosen_word = list(self._words.random_word())
        self._letters = []
        self._guess = list(" " * len(self._chosen_word))
        self._stage = 0

    def process_input(self):
        self.user_input = self.user_input.upper()
        return super().process_input()

    def valid_input(self):
        if self.user_input in self._letters:
            self.print(f"You've used that letter already.\n")
            return False
        return True

    def calculate_answer(self):
        # Randomly guess letters, checking that they haven't been used before
        answer = ''
        while answer == '':
            answer = choice(ascii_uppercase)
            if answer in self._letters:
                answer = ''

        return answer

    def update(self):
        super().update()
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
            return True
        else:
            self.print(f"Hard luck ... you lost. Correct Word: {''.join(self._chosen_word)}\n")
            return False

    def exit_game(self):
        self.print(f"You played {self._game_count} games and won {self._win_count} of them.\n")

game = Hangman({"letters":8, "P1":"Python", "display_game":False, "python_sleep":0, "auto_play_count": 100})
game.execute()
