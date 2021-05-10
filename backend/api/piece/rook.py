from api.piece.piece_interface import PieceInterface, Color


class Rook(PieceInterface):
    """
    Piece Rook
    """
    def __init__(self, game: 'ChessGame', color: Color, x: int, y: int):
        """
        The firstMove is true means the rook has not moved yet.
        If it is false, it means the rook has moved.
        Used for castling.
        :param game: a chess game instance
        :param color: indicate the color of the piece
        """
        super().__init__(game, color, x, y)
        self.firstMove = True

    def get_moves(self) -> list:
        """
        a list of all available moves of the piece in order
        by directions (up, right, down, left).
        """
        row, col = self.x, self.y
        directions = [[1, 0, 7 - row],      # up
                      [0, 1, 7 - col],      # right
                      [-1, 0, row],         # down
                      [0, -1, col]]         # left
        moves = []

        for direction in directions:
            ret_row, ret_col = row, col
            for index in range(direction[2]):
                ret_row += direction[0]
                ret_col += direction[1]

                tar_color = self.game.board[ret_row][ret_col].color
                if tar_color == self.color:
                    break

                if tar_color != Color.EMPTY:
                    moves.insert(0, (ret_row, ret_col))
                    break
                moves.append((ret_row, ret_col))

        return moves

    def to_string(self) -> str:
        """
        :return: "R" if the color of the piece is Color.WHITE. Otherwise, "r".
        """
        if self.color == Color.WHITE:
            return "R"
        return "r"
