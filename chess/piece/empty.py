from chess.piece.piece_interface import PieceInterface, Color
from chess.piece.coordinate import Coordinate


class Empty(PieceInterface):
    def get_moves(self) -> dict:
        return []

    def get_color(self) -> Color:
        return Color.EMPTY

    def to_string(self) -> str:
        return "*"
