from ConsoleGame import *
from cdkkWords import Words
from HangmanPyPlayer import *
from HangmanStages import *

class WordleGame(Game):
    def init(self):
        super().init()
        self.common_words = Words(word_length = self.length, common_words = True)
        self.allowed_words = Words(word_length = self.length, common_words = False)
        return True

    @property
    def length(self):
        return self.config.get("letters", 6)

    def start(self):
        super().start()
        self.chosen_word = self.common_words.random_word()
        self.guesses = []
        self.guesses_coloured = []

    def check(self, turn):
        if (self.allowed_words.contains_word(turn)):
            return ""
        else:
            return "Please enter a valid word"

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
        elif (len(self.guesses) == self.max_turns):
            # Player lost
            self.status = 99

# ----------------------------------------

class Wordle(cdkkConsoleGame):
    default_config = { "ConsoleGame": { "process_to_upper": True } }

    def __init__(self, init_config=None):
        super().__init__()
        self.game = WordleGame()
        self.update_configs(cdkkConsoleGame.default_config, Wordle.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]WORDLE[/blue] \n'
        self.instructions_str = f"Guess words with {self.game.length} letters."
        self.turn_pattern = f"^[a-zA-Z]{{{self.game.length}}}$"
        self.turn_pattern_error = f"Please enter a valid {self.config.get('letters')}-letter word.\n"

    def display(self):
        super().display()
        self._console.print(*self.game.guesses_coloured, sep="\n")
        self._console.print("")

    def end_game(self, outcome, players):
        if (outcome == 0 or outcome >= 99):
            self._console.print(f"Hard luck ... you used all {self.game.counts['turns']} guesses. Correct Word: {self.game.chosen_word}\n")
        else:
            if (players == 1):
                self._console.print(f"You beat WORDLE in {len(self.game.guesses)}/{self.game.max_turns} guesses.\n")
            else:
                self._console.print(f"{self.players[outcome-1]} beat WORDLE in {self.game.counts['turns']} guesses.\n")

    def exit_game(self):
        self._console.print(self.game_wins_msg())

wordle = Wordle({"Game":{"letters":5, "max_turns":6}})
wordle.execute()
