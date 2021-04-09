from chess.piece.piece_interface import PieceInterface, Color
from chess.piece.coordinate import Coordinate


class Pawn(PieceInterface):
    def en_passant(self, attack_col: int, row: int, col: int) -> bool:
        """
        Check if en passant is available for the capturing pawn at Coordinate(row, col)
        and the captured pawn at Coordinate(row, attack_col)
        En passant only occurred immediately after a pawn makes a move of two squares from its starting square,
        and it could have been captured by an enemy pawn had it advanced only one square.
        :param attack_col: the col of captured pawn
        :param row: the row of the capturing pawn ( same as the row of captured pawn)
        :param col: the col of the capturing pawn
        :return: True if en passant is available. Otherwise, False.
        """
        if len(self.game.history) == 0:
            return False
        last_move = self.game.history[-1]
        src_row = last_move["src"].get_tuple()[0]
        tar_row, tar_col = last_move["tar"].get_tuple()
        if type(last_move["src_piece"]) == Pawn and abs(src_row - tar_row) == 2 and row == tar_row and \
                abs(col - tar_col) == 1 and tar_col == attack_col:
            return True
        return False

    def get_moves(self) -> list:
        """
        :return: a list of all available moves and captures of a pawn.
        """
        coordinate = self.game.get_piece_coordinate(self)
        row, col = coordinate.get_tuple()
        direction = self.color.value
        moves = []

        # moves
        steps = 1
        if (self.color == Color.WHITE and row == 1) or (self.color == Color.BLACK and row == 6):
            steps = 2
        for step in range(1, steps + 1):
            ret_row = row + step * direction
            if PieceInterface.is_valid_coord(ret_row, col) and \
                    self.game.board[ret_row][col].get_color() == Color.EMPTY:
                moves.append(Coordinate(ret_row, col))
            else:
                break

        # captures
        attack_row = row + direction
        for attack_col in [col + 1, col - 1]:
            if PieceInterface.is_valid_coord(attack_row, attack_col) and \
                    ((self.game.board[attack_row][attack_col].get_color() not in [self.color, Color.EMPTY]) or
                     (self.en_passant(attack_col, row, col))):
                moves.append(Coordinate(attack_row, attack_col))
        return moves

    def to_string(self) -> str:
        """
        :return: "K" if the color of the piece is Color.WHITE. Otherwise, "k".
        """
        if self.color == Color.WHITE:
            return "P"
        return "p"
