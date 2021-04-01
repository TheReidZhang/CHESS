from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = -1
    EMPTY = 0


class PieceInterface:
    def __init__(self, game: 'ChessGame', color: Color):
        self.game = game
        self.color = color

    def get_moves(self) -> list:
        raise NotImplementedError

    def get_checked_moves(self):

        moves = self.get_moves()
        checked_moves = []
        if len(moves) > 0:
            coordinate = self.game.get_piece_coordinate(self)
            for move in moves:
                if not self.game.is_being_checked_after_move(coordinate, move):
                    checked_moves.append(move)
        return {"moves": checked_moves}

    def get_color(self) -> Color:
        raise NotImplementedError

    @staticmethod
    def is_valid_coord(row: int, col: int):
        return 0 <= row < 8 and 0 <= col < 8

    def to_string(self) -> str:
        raise NotImplementedError
