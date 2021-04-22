from api.piece.piece_interface import PieceInterface


class Empty(PieceInterface):
    def get_moves(self) -> list:
        """
        This is empty piece meaning at this square there is no pieces and no moves.
        :return: empty list meaning no moves
        """
        return []

    def to_string(self) -> str:
        """
        For debugging use, simply print *
        :return: a string "*"
        """
        return "*"
