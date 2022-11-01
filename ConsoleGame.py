# To Do: Add option to quit early
# To Do: Add game as param to display() and end_game()
# To Do: Add parameter types
# To Do: Migrate to full MVC/MVVM 
# https://realpython.com/python-dice-roll/

import re
import time
import sys
import os
github_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cdkk'))
sys.path.append(github_path)

from cdkkConfig import Config
from cdkkGame import Game
from cdkkConsole import Console
from cdkkConsole import Prompt

# ----------------------------------------

class cdkkPyPlayer:
    # Python Game Player
    default_config = {}

    def __init__(self, init_config={}):
        self.config = Config(cdkkPyPlayer.default_config)
        self.config.update(init_config)

    def init(self, game:Game):
        pass

    def calculate_turn(self, game:Game):
        pass


# ----------------------------------------

class cdkkConsoleGame:
    default_config = {
        "Game": { "players":1 }
        ,"ConsoleGame": {
            "process_to_upper": False  # True = Convert each turn to upper case
            ,"python_sleep": 1         # Time to sleep to simlaute Python input
            ,"exit_at_end": False      # True = Exit when the game ends; False = Ask to play again
            ,"auto_play_count": 0      # Number of games to play automatically (if asked)
        }
    }

    def __init__(self, init_config:dict = {}):
        self.config = Config()
        self.game = Game()
        self._console = Console()
        self.pyplayer = cdkkPyPlayer()

        self.update_configs(cdkkConsoleGame.default_config)
        self.update_configs(init_config)

        self.welcome_str = self.instructions_str = ""
        self.turn_pattern = self.turn_pattern_error = ""
        self.check_turn_error = "Invalid input: "
        self.player_names_str = "\nPlease enter each player's name."
        self.players = []

    def update_configs(self, *configs:dict):
        for cfg_dict in configs:
            self.config.update(cfg_dict.get("ConsoleGame", {}))
            self.game.config.update(cfg_dict.get("Game", {}))
            self._console.config.update(cfg_dict.get("Console", {}))
            self.pyplayer.config.update(cfg_dict.get("PyPlayer", {}))

    def init(self):
        # Return True if initialised OK
        game_ok = self.game.init()
        if game_ok:
            self.pyplayer.init(self.game)
        return game_ok

    def welcome(self):
        if self.welcome_str != '':
            self._console.clear_console()
            self._console.print(self.welcome_str)

    def instructions(self):
        if self.instructions_str != '':
            self._console.print(self.instructions_str)

    def start_game(self):
        self.game.start()

    def read_names(self):
        if len(self.players) == 0:
            for i in range(self.game.players):
                self.players.append(self.config.get(f"P{i+1}", f"P{i+1}"))

        if self.game.players < 2:
            return

        if self.player_names_str != '':
            self._console.print(self.player_names_str)

        for i in range(self.game.players):
            player = Prompt.ask(f"Player {i+1} \[{self.players[i]}] > ")
            if player != "":
                self.players[i] = player

    # def read_game_config(self):
    #     for key, value in self._game_config.items():
    #         if value == "":
    #             msg = f"{key} > "
    #         else:
    #             msg = f"{key} [{value}]> "
    #         cfg_value = Prompt.ask(msg)
    #         if cfg_value != "":
    #             self._game_config[key] = cfg_value

    def read_turn(self):
        if self.game.players > 1:
            msg = f"{self.players[self.game.current_player-1]} > "
        else:
            msg = "> "
        if self.players[self.game.current_player-1].upper() == "PYTHON":
            self._console.print(msg, end = '')
            return self.read_python_turn()
        else:
            return Prompt.ask(msg)

    def process_turn(self):
        # Process the input and return True if the input matches the pattern
        if self.next_turn == "?":
            self.instructions()
            return False
        if self.config.get("process_to_upper", False):
            self.next_turn = self.next_turn.upper()
        if self.turn_pattern != '':
            regex_check = re.search(self.turn_pattern, self.next_turn)
            if not regex_check and self.turn_pattern_error != '':
                self._console.print(self.turn_pattern_error)
            return regex_check
        return True

    def check_turn(self):
        # Return True if input is valid for the game
        valid_msg = self.game.check(self.next_turn)
        if valid_msg != "":
            self._console.print(self.check_turn_error + valid_msg + "\n")
        return (valid_msg == "")

    def read_python_turn(self):
        # Update display to look ike Python is responding
        answer = self.pyplayer.calculate_turn(self.game)
        if self.config.get("python_sleep") > 0 and not self.config.get("silent", False):
            time.sleep(self.config.get("python_sleep"))
        self._console.print(answer)
        return answer

    def update(self):
        # Update game elements and run game logic
        self.game.take(self.next_turn)

    def display(self):
        # Display the current version of the game
        pass

    def check_if_game_over(self):
        # Return True if the game is over
        return self.game.game_over

    def check_if_play_again(self):
        # Return True to play again
        if self.config.get("exit_at_end"):
            return False
        else:
            if self.config.get("auto_play_count") > 0:
                return (self.game.counts["games"] < self.config.get("auto_play_count"))
            ans = input("Do you want to play again? [Y/N] ").upper()
            return (ans == "Y")

    def end_game(self, outcome, players):
        # Display end of game infomration, such as whether the player won or lost
        # Outcome = 0 ... Draw. Outcome = 1+ ... Number of winning player
        pass

    def exit_game(self):
        # Any logic as the game exits
        pass

    def game_wins_msg(self):
        if self.game.players == 1:
            return (f"You played {self.game.counts['games']} games and won {self.game.counts['wins'][0]} of them.")
        else:
            msg = f"You played {self.game.counts['games']} games and the results were:\n"
            for i in range(self.game.players):
                msg += f"{self.players[i]} ... {self.game.counts['wins'][i]} wins\n"
            return (msg)

    def execute(self):
        # Console game loop
        self.init()

        if self.game.status < 0:
            self.welcome()
            self.instructions()
            self.read_names()
            self.start_game()
            self.display()

        while not self.game.game_over:
            while True:
                self.next_turn = self.read_turn()
                if self.process_turn():
                    if self.check_turn():
                        break

            self.update()
            self.display()
            if self.check_if_game_over():
                self.end_game(self.game.status, self.game.players)
                if self.check_if_play_again():
                    # Play again
                    self.start_game()
                    self.display()

        self.exit_game()


# ----------------------------------------

if __name__ == '__main__':
    pp = cdkkPyPlayer()
    cg = cdkkConsoleGame()
    print("Done")
