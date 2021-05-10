from api.piece.piece_interface import PieceInterface, Color


class Knight(PieceInterface):
    """
    Piece Knight
    """
    def get_moves(self) -> list:
        """
        a list of all available moves of the piece in order
        by directions (clockwise).
        """
        row, col = self.x, self.y
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
            tar_color = self.game.board[ret_row][ret_col].color
            if tar_color != self.color:
                if tar_color != Color.EMPTY:
                    moves.insert(0, (ret_row, ret_col))
                else:
                    moves.append((ret_row, ret_col))
        return moves

    def to_string(self) -> str:
        """
        :return: "N" if the color of the piece is Color.WHITE. Otherwise, "n".
        """
        if self.color == Color.WHITE:
            return "N"
        return "n"
