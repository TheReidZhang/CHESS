from api.piece.piece_interface import PieceInterface


class Empty(PieceInterface):
    def get_moves(self) -> list:
        return []

    def to_string(self) -> str:
        return "*"
