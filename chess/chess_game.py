from chess.piece.coordinate import Coordinate


class ChessGame:
    def __init__(self, fen="start"):
        self.fen = fen

    def en_passant(self):
        pass

    def castling(self):
        pass

    def update(self, src: Coordinate, tar: Coordinate) -> bool:
        pass

    def undo(self):
        pass

    def check_win(self):
        pass

    def switch_side(self):
        pass

    def get_fen(self):
        pass

    def to_string(self):
        pass
