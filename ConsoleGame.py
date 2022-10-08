from rich import print as rprint
from rich.prompt import Prompt
from rich.console import Console

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
        "exit_at_end": False    # True = Exit when the game ends; False = Ask to play again
    }

    def __init__(self, config=None):
        super().__init__()
        self._game_on = True
        self._config = {}
        self.update_config(cdkkConsoleGame.default_config)
        self.update_config(config)

    def init(self):
        # Return True if initialised OK
        return True

    def start_game(self):
        pass

    def read_input(self):
        return cdkkPrompt.ask("> ")

    def process_input(self):
        # Return True if input is OK
        return True

    def update(self):
        pass

    def display(self, first_time = False):
        pass

    def check_if_game_over(self):
        # Return True if game over
        return True

    def check_if_play_again(self):
        # Return True to play again
        if self.get_config("exit_at_end"):
            return False
        else:
            ans = input("Do you want to play again? [Y/N] ").upper()
            return (ans == "Y")

    def end_game(self):
        pass

    def exit_game(self):
        pass

    def execute(self):
        self._game_on = self.init()

        if self._game_on:
            self.start_game()
            self.display(first_time = True)

        while self._game_on:
            while True:
                self.user_input = self.read_input()
                if self.process_input():
                    break

            self.update()
            self.display(first_time = False)
            if self.check_if_game_over():
                self.end_game()
                self._game_on = self.check_if_play_again() 
                if self._game_on:
                    # Play again
                    self.start_game()
                    self.display(first_time = False)

        self.exit_game()
