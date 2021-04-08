from chess.piece.piece_interface import PieceInterface, Color


class Empty(PieceInterface):
    def get_moves(self) -> dict:
        return []

    def to_string(self) -> str:
        return "*"
