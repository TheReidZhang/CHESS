from enum import Enum
from coordinate import Coordinate
from chess.chess_game import ChessGame


class Color(Enum):
    WHITE = 0
    BLACK = 1


class PieceInterface:
    def __init__(self, game: ChessGame, color: Color, coordinate: Coordinate):
        self.game = game
        self.color = color
        self.coordinate = coordinate

    def can_move(self, coordinate: Coordinate) -> bool:
        raise NotImplementedError

    def get_captures(self) -> dict:
        raise NotImplementedError

    def get_moves(self) -> dict:
        raise NotImplementedError



