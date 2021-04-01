from chess.piece.piece_interface import PieceInterface, Color
from chess.piece.coordinate import Coordinate


class Knight(PieceInterface):
    def get_moves(self) -> dict:
        coordinate = self.game.get_piece_coordinate(self)
        row, col = coordinate.get_tuple()
        directions = [[1, 2],
                      [1, -2],
                      [-1, 2],
                      [-1, -2],
                      [2, 1],
                      [2, -1],
                      [-2, 1],
                      [-2, -1]]
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
            return "N"
        return "n"
