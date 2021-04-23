from api.piece.piece_interface import PieceInterface, Color
from api.piece.coordinate import Coordinate


class Knight(PieceInterface):
    """
    Piece Knight
    """
    def get_moves(self) -> list:
        """
        :return: a list of all available moves of the piece in order
        by directions (clockwise).
        """
        coordinate = self.game.get_piece_coordinate(self)
        row, col = coordinate.get_tuple()
        directions = [[2, 1],
                      [1, 2],
                      [-1, 2],
                      [-2, 1],
                      [-2, -1],
                      [-1, -2],
                      [1, -2],
                      [2, -1]]
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

    def to_string(self) -> str:
        """
        :return: "N" if the color of the piece is Color.WHITE. Otherwise, "n".
        """
        if self.color == Color.WHITE:
            return "N"
        return "n"
