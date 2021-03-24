from piece_interface import PieceInterface, Color
from coordinate import Coordinate
from chess.chess_game import ChessGame


class Queen(PieceInterface):
    def __init__(self, game: ChessGame, color: Color, coordinate: Coordinate):
        super(game, color, coordinate)

    def can_move(self, coordinate: Coordinate) -> bool:
        raise NotImplementedError

    def get_captures(self) -> dict:
        raise NotImplementedError

    def get_moves(self) -> dict:
        raise NotImplementedError