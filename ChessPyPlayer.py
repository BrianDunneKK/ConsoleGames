from random import choice
from string import ascii_uppercase
from ConsoleGame import cdkkPyPlayer
from ConsoleGame import Game
import chess.engine

class ChessPyPlayer(cdkkPyPlayer):
    def calculate_turn(self, game: Game) -> str:
        engine = chess.engine.SimpleEngine.popen_uci("C:\\Apps\\stockfish_15.1\\stockfish-windows-2022-x86-64-avx2.exe")
        limit = chess.engine.Limit(time=2.0)
        play_result = engine.play(game.chess, limit)
        return(play_result.move.uci())

