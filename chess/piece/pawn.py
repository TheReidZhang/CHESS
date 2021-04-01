from chess.piece.piece_interface import PieceInterface, Color
from chess.piece.coordinate import Coordinate


class Pawn(PieceInterface):
    def en_passant(self, attack_col: int, row: int, col: int):
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

    def get_color(self) -> Color:
        return self.color

    def to_string(self) -> str:
        if self.color == Color.WHITE:
            return "P"
        return "p"
