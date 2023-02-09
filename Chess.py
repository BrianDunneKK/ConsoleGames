from ConsoleGame import *
from cdkkBoard import *
from cdkkGamePiece import GamePieceNM 
import chess
from ChessPyPlayer import *

class ChessPiece(GamePieceNM):
    # Upper case = White; Lower case = Black
    symbols = {0: " ", 1: "P", 2:"N", 3:"B", 4:"R", 5:"Q", 6:"K", 11: "p", 12:"n", 13:"b", 14:"r", 15:"q", 16:"k"}
    icons = {0: " ", 1: "♙", 2:"♘", 3:"♗", 4:"♖", 5:"♕", 6:"♔", 11: chr(9823), 12:"♞", 13:"♝", 14:"♜", 15:"♛", 16:"♚"}
    # Need to use chr(9823) as '♟︎' is 2 characters

    def __init__(self, code: int = 0, symbol: str = "", symbol_dict: dict = {}, context: dict = {}):
        super().__init__(code, value = -999, symbol_dict=symbol_dict, random_code=False, context=context, ncols=5, mrows=3)

class ChessBoard(Board):
    def __init__(self, symbol_dict: dict = {}):
        super().__init__(xsize=8, ysize=8, symbol_dict=symbol_dict)
        bk0 = "default on orange4"
        bk1 = "default on cornsilk1"
        chequered = [[bk0, bk1],[bk1, bk0]]
        self.set_style_pattern(chequered)

    def create_piece(self, code: int = 0, value: int = -1) -> ChessPiece:
        return ChessPiece(code = code, symbol_dict=self._symbols, context={"style":"bold"})

# ----------------------------------------

class ChessGame(Game):
    def init(self):
        super().init()
        if self.config.get("pieces", "symbols") == "symbols":
            self._pieces = ChessPiece.symbols
        else:
            self._pieces = ChessPiece.icons
        self.board = ChessBoard(self._pieces)
        self.board.set(0,0,4)
        self.board.set(0,1,3)
        return True

    def start(self) -> None:
        super().start()
        self.chess = chess.Board()
        self.board.clear_all()
        self.map_model()

    def map_model(self):
        if self.config.get("pieces", "symbols") == "symbols":
            strs = str(self.chess)
        else:
            strs = self.chess.unicode(empty_square=".")
        strs = strs.replace(" ", "")
        strs = strs.replace(".", " ")
        strs = strs.split(sep="\n")
        strs = [list(s) for s in strs]
        self.board.set_symbol_mask(strs)

    def check(self, turn) -> str:
        move = chess.Move.from_uci(turn)
        if move in self.chess.legal_moves:
            return ""
        return ("Please enter a legal move")

    def take(self, turn) -> None:
        move = chess.Move.from_uci(turn)
        self.chess.push(move)  # Make the move
        self.map_model()

# ----------------------------------------

class Chess(cdkkConsoleGame):
    default_config = { "ConsoleGame": { "process_to_lower": True } }

    def __init__(self, init_config={}) -> None:
        super().__init__()
        self.game = ChessGame()
        self.pyplayer = ChessPyPlayer()
        self.update_configs(cdkkConsoleGame.default_config, Chess.default_config, init_config)
        self._console.config.copy("silent", self.config, False)

        self.welcome_str = '\n [red]WELCOME[/red] [green]TO[/green] [blue]Chess[/blue] \n'
        self.instructions_str = "Enter the start and end grid referene."
        self.turn_pattern = "^[A-Ha-h][1-8][A-Ha-h][1-8]$"
        self.turn_pattern_error = "Please enter a valid start and end grid reference.\n"

    def display(self) -> None:
        super().display()
        self._console.print("")
        self._console.print(*self.game.board.richtext(borders=Board.borders_outside1, gridref = "yellow"), sep="\n")
        self._console.print("")


chess_app = Chess({"Game":{"pieces":"icons", "players":2}, "ConsoleGame":{"P2":"Python"}})
#chess_app = Chess({ "Game":{"pieces":"symbols"} })
chess_app.execute()
