from api.piece.piece_interface import PieceInterface, Color
from api.piece.coordinate import Coordinate
from api.piece.rook import Rook


class King(PieceInterface):
    def __init__(self, game: 'ChessGame', color: Color):
        """
        The firstMove is true means the king has not moved yet.
        If it is false, it means the king has moved.
        Used for castling.
        :param game: a chess game instance
        :param color: indicate the color of the piece
        """
        super().__init__(game, color)
        self.firstMove = True   # True if the king has not been moved

    def get_moves(self) -> list:
        """
        :return: a list of all available moves of the piece in order
        by directions (up, upper right, right, lower right, down, lower left, left, upper left).
        """
        coordinate = self.game.get_piece_coordinate(self)
        row, col = coordinate.get_tuple()
        directions = [[1, 0],       # up
                      [1, 1],       # upper right
                      [0, 1],       # right
                      [-1, 1],      # lower right
                      [-1, 0],      # down
                      [-1, -1],     # lower left
                      [0, -1],      # left
                      [1, -1]]      # upper left
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
        :return: "K" if the color of the piece is Color.WHITE. Otherwise, "k".
        """
        if self.color == Color.WHITE:
            return "K"
        return "k"

    def get_checked_moves(self) -> dict:
        """
        :return: a dictionary. Key is "moves", and value is a list of all available moves that will not
        make the king being checked after the move.
        """
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
        """
        Castling is available if the following conditions are all met:
        1. The king is not being checked.
        2. The king and the rook have not been moved.
        3. There is no pieces between the king and the rook.
        4. The king will not be into check.

        :param king_side: True if castling with the rook at king side. Otherwise, False. The default value is False.
        :return: True if castling available. Otherwise, False.
        """
        if self.game.is_being_checked() or not self.firstMove or self.rook_has_moved(king_side) \
                or self.pieces_between_king_and_rook(king_side) or self.into_checked(king_side):
            return False
        return True

    def pieces_between_king_and_rook(self, king_side: bool) -> bool:
        """
        Check if there is any piece between the king and the rook.

        :param king_side: True if castling with the rook at king side. Otherwise, False.
        :return: True if there a piece between the king and the rook. Otherwise, False.
        """
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
        """
        Check if the king will be into check.
        :param king_side: True if castling with the rook at king side. Otherwise, False.
        :return: True if the king will be into check. Otherwise, False.
        """
        row = 0 if self.color == Color.WHITE else 7
        col = 5 if king_side else 2

        if self.game.is_being_checked_after_move(Coordinate(row, 4), Coordinate(row, col)):
            return True
        if self.game.is_being_checked_after_move(Coordinate(row, 4), Coordinate(row, col+1)):
            return True
        return False

    def rook_has_moved(self, king_side: bool) -> bool:
        """
        Check if the rook has been moved.
        :param king_side: True if castling with the rook at king side. Otherwise, False.
        :return: True if the rook has been moved. Otherwise, False.
        """
        rook_row = 0 if self.color == Color.WHITE else 7
        rook_col = 7 if king_side else 0

        if type(self.game.board[rook_row][rook_col]) != Rook:
            return True
        if not self.game.board[rook_row][rook_col].firstMove:
            return True
        return False
