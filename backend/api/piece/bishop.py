from api.piece.piece_interface import PieceInterface, Color


class Bishop(PieceInterface):
    """
    Piece Bishop
    """
    def get_moves(self) -> list:
        """
        :return: a list of all available moves of the piece in order
        by directions (upper right, lower right, upper left, lower left).
        """
        row, col = self.x, self.y
        directions = [[1, 1],       # upper right
                      [-1, 1],      # lower right
                      [-1, -1],     # lower left
                      [1, -1]]      # upper left
        moves = []

        for direction in directions:
            ret_row = row + direction[0]
            ret_col = col + direction[1]

            while PieceInterface.is_valid_coord(ret_row, ret_col):
                tar_color = self.game.board[ret_row][ret_col].color
                if tar_color == self.color:
                    break

                if tar_color != Color.EMPTY:
                    moves.insert(0, (ret_row, ret_col))
                    break
                moves.append((ret_row, ret_col))

                ret_row += direction[0]
                ret_col += direction[1]
        return moves

    def to_string(self) -> str:
        """
        :return: "B" if the color of the piece is Color.WHITE. Otherwise, "b".
        """
        if self.color == Color.WHITE:
            return "B"
        return "b"
