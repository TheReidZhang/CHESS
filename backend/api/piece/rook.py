from api.piece.piece_interface import PieceInterface, Color
from api.piece.coordinate import Coordinate


class Rook(PieceInterface):
    """
    Piece Rook
    """
    def __init__(self, game: 'ChessGame', color: Color):
        """
        The firstMove is true means the rook has not moved yet.
        If it is false, it means the rook has moved.
        Used for castling.
        :param game: a chess game instance
        :param color: indicate the color of the piece
        """
        super().__init__(game, color)
        self.firstMove = True

    def get_moves(self) -> list:
        """
        :return: a list of all available moves of the piece in order
        by directions (up, right, down, left).
        """
        coordinate = self.game.get_piece_coordinate(self)
        row, col = coordinate.get_tuple()
        directions = [[1, 0],   # up
                      [0, 1],  # right
                      [-1, 0],  # down
                      [0, -1]]  # left
        moves = []

        for direction in directions:
            ret_row = row + direction[0]
            ret_col = col + direction[1]

            while PieceInterface.is_valid_coord(ret_row, ret_col):
                tar_color = self.game.board[ret_row][ret_col].get_color()
                if tar_color == self.color:
                    break
                moves.append(Coordinate(ret_row, ret_col))
                if tar_color != Color.EMPTY:
                    break
                ret_row += direction[0]
                ret_col += direction[1]
        return moves

    def to_string(self) -> str:
        """
        :return: "R" if the color of the piece is Color.WHITE. Otherwise, "r".
        """
        if self.color == Color.WHITE:
            return "R"
        return "r"
