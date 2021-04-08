from chess.piece.piece_interface import PieceInterface, Color
from chess.piece.coordinate import Coordinate
from chess.chess_game import ChessGame


class Rook(PieceInterface):
    def __init__(self, game: 'ChessGame', color: Color):
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
