from chess.piece.piece_interface import PieceInterface, Color
from chess.piece.coordinate import Coordinate
from chess.piece.rook import Rook


class King(PieceInterface):
    def __init__(self, game: 'ChessGame', color: Color):
        super().__init__(game, color)
        self.firstMove = True

    def get_moves(self) -> dict:
        coordinate = self.game.get_piece_coordinate(self)
        row, col = coordinate.get_tuple()
        directions = [[1, -1],
                      [1, 1],
                      [-1, 1],
                      [-1, -1],
                      [0, 1],
                      [0, -1],
                      [1, 0],
                      [-1, 0]]
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
            return "K"
        return "k"

    def get_checked_moves(self):
        moves = self.get_moves()
        checked_moves = []
        if len(moves) > 0:
            coordinate = self.game.get_piece_coordinate(self)
            for move in moves:
                if not self.game.is_being_checked_after_move(coordinate, move):
                    checked_moves.append(move)
        row = 0 if self.color == Color.WHITE else 7

        if self.castling(king_side=True):
            checked_moves.append(Coordinate(row, 6))
        if self.castling(king_side=False):
            checked_moves.append(Coordinate(row, 2))
        return {"moves": checked_moves}

    def castling(self, king_side=True) -> bool:
        if self.game.is_being_checked() or not self.firstMove or self.rook_has_moved(king_side) \
                or self.pieces_between_king_and_rook(king_side) or self.into_checked(king_side):
            return False
        return True

    def pieces_between_king_and_rook(self, king_side: bool) -> bool:
        row = 0 if self.color == Color.WHITE else 7
        if king_side:
            if (self.game.board[row][5].color, self.game.board[row][6].color) != (Color.EMPTY, Color.EMPTY):
                return True
        else:   # queen side
            if (self.game.board[row][1].color,
                    self.game.board[row][2].color,
                    self.game.board[row][3].color) != (Color.EMPTY, Color.EMPTY, Color.EMPTY):
                return True
        return False

    def into_checked(self, king_side: bool) -> bool:
        row = 0 if self.color == Color.WHITE else 7
        col = 5 if king_side else 2

        if self.game.is_being_checked_after_move(Coordinate(row, 4), Coordinate(row, col)):
            return True
        if self.game.is_being_checked_after_move(Coordinate(row, 4), Coordinate(row, col+1)):
            return True
        return False

    def rook_has_moved(self, king_side: bool) -> bool:
        rook_row = 0 if self.color == Color.WHITE else 7
        rook_col = 7 if king_side else 0

        if type(self.game.board[rook_row][rook_col]) != Rook:
            return True
        if not self.game.board[rook_row][rook_col].firstMove:
            return True
        return False
