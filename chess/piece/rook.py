from chess.piece.piece_interface import PieceInterface, Color
from chess.piece.coordinate import Coordinate


class Rook(PieceInterface):
    def __init__(self, game: 'ChessGame', color: Color):
        super().__init__(game, color)
        self.firstMove = True

    def get_moves(self) -> list:
        coordinate = self.game.get_piece_coordinate(self)
        row, col = coordinate.get_tuple()
        directions = [[1, 0],
                      [-1, 0],
                      [0, 1],
                      [0, -1]]
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

    def get_color(self) -> Color:
        return self.color

    def to_string(self) -> str:
        if self.color == Color.WHITE:
            return "R"
        return "r"
