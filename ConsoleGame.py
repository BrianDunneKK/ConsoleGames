# To Do: Add option to quit early
# To Do: Add game as param to display() and end_game()
# To Do: Add parameter types
# To Do: Migrate to full MVC/MVVM 

from operator import le
from rich import print as rprint
from rich.prompt import Prompt
from rich.console import Console
import re
import time

class cdkkConfig:
    def __init__(self, init_config=None):
        self.config = {}
        if init_config != None:
            self.config.update(init_config)

    def get_config(self, attribute, default=None):
        return self.config.get(attribute, default)

    def set_config(self, attribute, new_value):
        if attribute is not None:
            self.config[attribute] = new_value

    def update_config(self, updated__configs):
        if updated__configs != None:
            for key, value in updated__configs.items():
                self.config[key] = value

    def copy_config(self, attribute, from_config, default):
        self.set_config(attribute, from_config.get_config(attribute, default))

# ----------------------------------------

class cdkkPrompt(Prompt):
    prompt_suffix = ""

class cdkkConsole(cdkkConfig):
    default_config = {
        "silent": False           # True = Hide all console output
        ,"cls_first_print": True  # True = Clear the screen when print is first called
    }
    console = Console()

    def __init__(self, init_config=None):
        super().__init__(cdkkConsole.default_config)
        self.update_config(init_config)
        self.clear_next_print = self.get_config("cls_first_print", False)

    def print(self, *args, **kwargs):
        if self.clear_next_print:
            self.clear_console()
            self.clear_next_print = False
        if not self.get_config("silent", False):
            cdkkConsole.console.print(*args, **kwargs, highlight = False)

    def clear_console(self):
        if not self.get_config("silent", False):
                self.console.clear()

# ----------------------------------------

class cdkkGame(cdkkConfig):
    # Methods to update in sub-classes: init, start, check, update
    default_config = {}

    def __init__(self, init_config=None):
        super().__init__(cdkkGame.default_config)
        self.update_config(init_config)
        self.game_count = self.turn_count = self.current_player = 0
        self.num_players = self.get_config("players", 1)
        self.player_wins = [0] * self.num_players
        self.status = -2
            # Game status:
            #   -2 = No game in progress
            #   -1 = Game in progress
            #    0 = Game over - Draw
            # 1-98 = Game over - Win - Number of winning player
            #   99 = Game over - Loss
            # 100+ = Game over - Error number

    def game_over(self):
        # Return True if the game is over
        return (self.status >= 0)

    def take(self, turn):
        # Take turn for player
        self.update(turn)
        if not self.game_over():
            self.turn_count += 1
            self.current_player += 1
            if self.current_player > self.num_players:
                self.current_player = 1
        else:
            if (self.status > 0 and self.status < 99):
                self.player_wins[self.current_player-1] += 1

    def init(self):
        # Return True if initialised OK
        return True

    def start(self):
        self.game_count += 1
        self.turn_count = 1
        self.current_player = 1
        self.status = -1

    def check(self, turn):
        # Return True if this turn is valid for the game
        return True

    def update(self, turn):
        # Run game logic, update game elements including status
        pass
    
# ----------------------------------------

class cdkkPyPlayer(cdkkConfig):
    # Python Game Player
    default_config = {}

    def __init__(self, init_config=None):
        super().__init__(cdkkPyPlayer.default_config)
        self.update_config(init_config)

    def calculate_turn(self, game):
        pass


# ----------------------------------------

class cdkkConsoleGame(cdkkConfig):
    default_config = {
        "players":1
        ,"process_to_upper": False # True = Convert each turn to upper case
        ,"python_sleep": 1         # Time to sleep to simlaute Python input
        ,"exit_at_end": False      # True = Exit when the game ends; False = Ask to play again
        ,"auto_play_count": 0      # Number of games to play automatically (if asked)
    }

    def __init__(self, init_config=None):
        super().__init__()
        self.update_config(cdkkConsoleGame.default_config)
        self.update_config(init_config)

        self.game = cdkkGame(self.config)
        self._console = cdkkConsole(self.config)
        self.pyplayer = cdkkPyPlayer()
        # self._console.copy_config("silent", self, False)

        self.welcome_str = self.instructions_str = ""
        self.turn_pattern = self.turn_pattern_error = self.check_turn_error = ""
        self.player_names_str = "\nPlease enter each player's name."
        self.players = []

    def init(self):
        # Return True if initialised OK
        return self.game.init()

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
            for i in range(self.game.num_players):
                self.players.append(self.get_config(f"P{i+1}", f"P{i+1}"))

        if self.game.num_players < 2:
            return

        if self.player_names_str != '':
            self._console.print(self.player_names_str)

        for i in range(self.game.num_players):
            player = cdkkPrompt.ask(f"Player {i+1} \[{self.players[i]}] > ")
            if player != "":
                self.players[i] = player

    # def read_game_config(self):
    #     for key, value in self._game_config.items():
    #         if value == "":
    #             msg = f"{key} > "
    #         else:
    #             msg = f"{key} [{value}]> "
    #         cfg_value = cdkkPrompt.ask(msg)
    #         if cfg_value != "":
    #             self._game_config[key] = cfg_value

    def read_turn(self):
        if self.game.num_players > 1:
            msg = f"{self.players[self.game.current_player-1]} > "
        else:
            msg = "> "
        if self.players[self.game.current_player-1].upper() == "PYTHON":
            self._console.print(msg, end = '')
            return self.read_python_turn()
        else:
            return cdkkPrompt.ask(msg)

    def process_turn(self):
        # Process the input and return True if the input matches the pattern
        if self.next_turn == "?":
            self.instructions()
            return False
        if self.get_config("process_to_upper", False):
            self.next_turn = self.next_turn.upper()
        if self.turn_pattern != '':
            regex_check = re.search(self.turn_pattern, self.next_turn)
            if not regex_check and self.turn_pattern_error != '':
                self._console.print(self.turn_pattern_error)
            return regex_check
        return True

    def check_turn(self):
        # Return True if input is valid for the game
        valid_turn = self.game.check(self.next_turn)
        if not valid_turn and self.check_turn_error != '':
            self._console.print(self.check_turn_error)
        return valid_turn

    def read_python_turn(self):
        # Update display to look ike Python is responding
        answer = self.pyplayer.calculate_turn(self.game)
        if self.get_config("python_sleep") > 0 and not self.get_config("silent", False):
            time.sleep(self.get_config("python_sleep"))
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
        return self.game.game_over()

    def check_if_play_again(self):
        # Return True to play again
        if self.get_config("exit_at_end"):
            return False
        else:
            if self.get_config("auto_play_count") > 0:
                return (self.game.game_count < self.get_config("auto_play_count"))
            ans = input("Do you want to play again? [Y/N] ").upper()
            return (ans == "Y")

    def end_game(self, outcome):
        # Display end of game infomration, such as whether the player won or lost
        # Outcome = 0 ... Draw. Outcome = 1+ ... Number of winning player
        pass

    def exit_game(self):
        # Any logic as the game exits
        pass

    def games_wins_msg(self):
        if self.game.num_players == 1:
            return (f"You played {self.game.game_count} games and won {self.game.player_wins[0]} of them.")
        else:
            msg = f"You played {self.game.game_count} games and the results were:\n"
            for i in range(self.game.num_players):
                msg += f"{self.players[i]} ... {self.game.player_wins[i]} wins\n"
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

        while not self.game.game_over():
            while True:
                self.next_turn = self.read_turn()
                if self.process_turn():
                    if self.check_turn():
                        break

            self.update()
            self.display()
            if self.check_if_game_over():
                self.end_game(self.game.status, self.game.num_players)
                if self.check_if_play_again():
                    # Play again
                    self.start_game()
                    self.display()

        self.exit_game()
