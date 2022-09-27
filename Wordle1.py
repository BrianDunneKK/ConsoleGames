import csv
import sys
from random import choice

cfg = {"letters": 5, "guesses": 6, "nocolour":"\033[0m", "green":"\033[0;32m", "yellow":"\033[0;33m"}

# -----

def correct_place(letter):
    return f'{cfg["green"]}{letter}{cfg["nocolour"]} '

def correct_letter(letter):
    return f'{cfg["yellow"]}{letter}{cfg["nocolour"]} '

def incorrect_letter(letter):
    return f'{letter} '

def check_guess(guess, answer):
    guessed = []
    for i, letter in enumerate(guess):
        if answer[i] == guess[i]:
            guessed += correct_place(letter)
        elif letter in answer:
            guessed += correct_letter(letter)
        else:
            guessed += incorrect_letter(letter)

    return ''.join(guessed)

# -----

word_options = []
with open("wordlist.csv", newline='') as f:
    csv_rdr = csv.reader(f)
    for row in csv_rdr:
        word =  row[0]
        if (len(word) == cfg['letters']):
            word_options.append(word.upper())

chosen_word = choice(word_options)
end_of_game = False
already_guessed = []
all_words_guessed = []

print(f'\n WELCOME TO WORDLE \n')
print("You may start guessing\n")

while not end_of_game:
    guess = input("\nEnter your guess: ").upper()
    while len(guess) != cfg['letters'] or guess not in word_options:
        print(f'Please enter a valid {cfg["letters"]}-letter word!!\n')
        guess = input("\nEnter your guess: ").upper()

    already_guessed.append(guess)
    guessed = check_guess(guess, chosen_word)
    all_words_guessed.append(guessed)

    print(*all_words_guessed, sep="\n")
    if guess == chosen_word or len(already_guessed) == cfg['guesses']:
        end_of_game = True

if len(already_guessed) == cfg['guesses'] and guess != chosen_word:
    print(f"\nHard luck ... you used all {cfg['guesses']} guesses. Correct Word: {chosen_word}")
else:
    print(f"\nYou beat WORDLE {len(already_guessed)}/{cfg['guesses']}\n")
    