# To Do: Change display_game config to hide_output and move logic to cdkkConsole and cdkkPrompt
# To Do: Add option to quit early

from rich import print as rprint
from rich.prompt import Prompt
from rich.console import Console
import re
import time

class cdkkPrompt(Prompt):
    prompt_suffix = ""

class cdkkConsole:
    default_config = {}
    console = Console()

    def __init__(self, config=None):
        super().__init__()
        self._config = {}
        self.update_config(cdkkConsole.default_config)
        self.update_config(config)

    def get_config(self, attribute, default=None):
        return self._config.get(attribute, default)

    def set_config(self, attribute, new_value):
        if attribute is not None:
            self._config[attribute] = new_value

    def update_config(self, *updated__configs):
        for cfg in updated__configs:
            if cfg is not None:
                for key, value in cfg.items():
                    self.set_config(key, value)

    def print(self, *args, **kwargs):
        cdkkConsole.console.print(*args, **kwargs, highlight = False)
        # rprint(*args, **kwargs)


class cdkkConsoleGame(cdkkConsole):
    default_config = {
        "players":1
        ,"display_game": True   # True = Display the game each loop
        ,"python_sleep": 1      # Time to sleep to simlaute Python input
        ,"exit_at_end": False   # True = Exit when the game ends; False = Ask to play again
        ,"auto_play_count": 0   # Number of games to play automatically (if asked)
    }

    def __init__(self, config=None):
        super().__init__()
        self._game_on = True
        self._config = {}
        self.update_config(cdkkConsoleGame.default_config)
        self.update_config(config)
        self._game_config = {}
        self._game_count = 0
        self._win_count = 0
        self.welcome_str = ""
        self.player_names_str = "\nPlease enter each player's name."
        self.instructions_str = ""
        self.input_pattern = ""
        self.input_error = ""
        self.players = []
        for i in range(self.get_config("players")):
            self.players.append(self.get_config(f"P{i+1}", f"P{i+1}"))

    def init(self):
        # Return True if initialised OK
        return True

    def welcome(self):
        if self.welcome_str != '':
            self.console.clear()
            self.print(self.welcome_str)

    def instructions(self):
        if self.instructions_str != '':
            self.print(self.instructions_str)

    def start_game(self):
        self._input_count = 0
        self._game_count += 1
        self.current_player = 1

    def read_names(self):
        if self.get_config("players") < 2:
            return

        if self.player_names_str != '':
            self.print(self.player_names_str)

        for i in range(self.get_config("players")):
            player = cdkkPrompt.ask(f"Player {i+1} \[{self.players[i]}] > ")
            if player != "":
                self.players[i] = player

    def read_game_config(self):
        for key, value in self._game_config.items():
            if value == "":
                msg = f"{key} > "
            else:
                msg = f"{key} [{value}]> "
            cfg_value = cdkkPrompt.ask(msg)
            if cfg_value != "":
                self._game_config[key] = cfg_value

    def read_input(self):
        if self.get_config("players") > 1:
            msg = f"{self.players[self.current_player-1]} > "
        else:
            msg = "> "
        if self.players[self.current_player-1].upper() == "PYTHON":
            self.print(msg, end = '')
            return self.read_python_input()
        else:
            return cdkkPrompt.ask(msg)

    def process_input(self):
        # Process the input and return True if the input matches the pattern
        if self.user_input == "?":
            self.instructions()
            return False
        if self.input_pattern != '':
            regex_check = re.search(self.input_pattern, self.user_input)
            if not regex_check and self.input_error != '':
                self.print(self.input_error)
            return regex_check
        return True

    def valid_input(self):
        # Return True if input is valid for the game
        return True

    def read_python_input(self):
        # Update display to look ike Python is responding
        answer = self.calculate_answer()
        if self.get_config("python_sleep") > 0:
            time.sleep(self.get_config("python_sleep"))
        self.print(answer)
        return answer

    def calculate_answer(self):
        # Logic to calculate the computer's answer
        return "python"

    def update(self):
        # Update game elements and run game logic
        self._input_count += 1
        self.current_player += 1
        if self.current_player > self.get_config("players"):
            self.current_player = 1

    def display(self, first_time = False):
        # Display the current version of the game
        return self.get_config("display_game")

    def check_if_game_over(self):
        # Return True if the game is over
        return True

    def check_if_play_again(self):
        # Return True to play again
        if self.get_config("exit_at_end"):
            return False
        else:
            if self.get_config("auto_play_count") > 0:
                return (self._game_count < self.get_config("auto_play_count"))
            ans = input("Do you want to play again? [Y/N] ").upper()
            return (ans == "Y")

    def end_game(self):
        # Display end of game infomration, such as whether the player won or lost
        # Return True if the player won
        return True

    def exit_game(self):
        # Any logic as the game exits
        pass

    def execute(self):
        # Console game loop
        self._game_on = self.init()

        if self._game_on:
            self.welcome()
            self.instructions()
            self.start_game()
            self.read_names()
            self.display(first_time = True)

        while self._game_on:
            while True:
                self.user_input = self.read_input()
                if self.process_input():
                    if self.valid_input():
                        break

            self.update()
            self.display(first_time = False)
            if self.check_if_game_over():
                if self.end_game():
                    self._win_count += 1
                self._game_on = self.check_if_play_again() 
                if self._game_on:
                    # Play again
                    self.start_game()
                    self.read_names()
                    self.display(first_time = False)

        self.exit_game()
