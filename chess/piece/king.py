from chess.piece.piece_interface import PieceInterface, Color
from chess.piece.coordinate import Coordinate


class King(PieceInterface):
    def __init__(self, game: 'ChessGame', color: Color):
        super().__init__(game, color)
        self.firstMove = True

    def get_moves(self) -> dict:
        coordinate = self.game.get_piece_coordinate(self)
        row, col = coordinate.get_tuple()
        directions = [[1, -1],
                      [1, 1],
                      [-1, 1],
                      [-1, -1],
                      [0, 1],
                      [0, -1],
                      [1, 0],
                      [-1, 0]]
        moves = []

        for direction in directions:
            ret_row = row + direction[0]
            ret_col = col + direction[1]
            if not PieceInterface.is_valid_coord(ret_row, ret_col):
                continue
            tar_color = self.game.board[ret_row][ret_col].get_color()
            if tar_color != self.color:
                moves.append(Coordinate(ret_row, ret_col))

        return moves

    def get_color(self) -> Color:
        return self.color

    def to_string(self) -> str:
        if self.color == Color.WHITE:
            return "K"
        return "k"

    def get_checked_moves(self):
        moves = self.get_moves()
        checked_moves = []
        if len(moves) > 0:
            coordinate = self.game.get_piece_coordinate(self)
            for move in moves:
                if not self.game.is_being_checked_after_move(coordinate, move):
                    checked_moves.append(move)
        return {"moves": checked_moves}