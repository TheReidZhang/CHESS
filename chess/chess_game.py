from chess.piece.coordinate import Coordinate
from chess.piece.empty import Empty
from chess.piece.pawn import Pawn
from chess.piece.knight import Knight
from chess.piece.bishop import Bishop
from chess.piece.king import King
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.piece.piece_interface import Color, PieceInterface
from colorama import Fore, Style


# noinspection PyTypeChecker
class ChessGame:
    def __init__(self, fen="start"):
        self.board = []
        self.empty_cell = Empty(None, Color.EMPTY)
        self.history = []
        # add
        self.count = 1
        self.half_move_clock = 0
        self.full_move_clock = 1
        self.en_passant_target_notation = "-"
        ##
        for row in range(8):
            row_list = []
            for col in range(8):
                row_list.append(self.empty_cell)
            self.board.append(row_list)
        self.side = Color.WHITE

        if fen == "start":
            for col in range(8):
                self.board[1][col] = Pawn(self, Color.WHITE)
                self.board[6][col] = Pawn(self, Color.BLACK)
            for row, color in [(0, Color.WHITE), (7, Color.BLACK)]:
                self.board[row][0] = Rook(self, color)
                self.board[row][7] = Rook(self, color)
                self.board[row][1] = Knight(self, color)
                self.board[row][6] = Knight(self, color)
                self.board[row][2] = Bishop(self, color)
                self.board[row][5] = Bishop(self, color)
                self.board[row][3] = Queen(self, color)
                self.board[row][4] = King(self, color)

    def get_checked_moves(self, coordinate: Coordinate) -> dict:
        row, col = coordinate.get_tuple()
        piece = self.board[row][col]
        if piece.get_color() != self.side:
            return {"moves": []}
        ret = piece.get_checked_moves()["moves"]
        ret = Coordinate.encode_list(ret)
        return {"moves": ret}

    def update(self, src: Coordinate, tar: Coordinate) -> bool:
        src_row, src_col = src.get_tuple()
        src_piece = self.board[src_row][src_col]
        if self.board[src_row][src_col].get_color() == self.side and \
                tar in src_piece.get_checked_moves()["moves"]:
            tar_row, tar_col = tar.get_tuple()
            tar_piece = self.board[tar_row][tar_col]
            castling = False
            en_passant = False
            self.en_passant_target_notation = "-"
            # add trace for en_passant target square notation
            if type(src_piece) == Pawn:
                step = tar_row - src_row
                if abs(step) == 2 and src_col == tar_col:
                    if step > 0:
                        self.en_passant_target_notation = Coordinate(tar_row - 1, tar_col).encode()
                    else:
                        self.en_passant_target_notation = Coordinate(tar_row + 1, tar_col).encode()
            #
            if type(src_piece) == King and abs(src_col - tar_col) == 2:
                castling = True
                if tar_col > src_col:
                    rook = self.board[src_row][7]
                    self.board[tar_row][tar_col - 1] = rook
                    self.board[src_row][7] = self.empty_cell
                else:
                    rook = self.board[src_row][0]
                    self.board[tar_row][tar_col + 1] = rook
                    self.board[src_row][0] = self.empty_cell
            elif type(src_piece) == Pawn and src_col != tar_col and tar_piece == self.empty_cell:
                en_passant = True
                last_pawn_row, last_pawn_col = self.history[-1]["tar"].get_tuple()
                self.board[last_pawn_row][last_pawn_col] = self.empty_cell
            # add
            if self.count % 2 == 0:
                self.full_move_clock += 1
            self.count += 1
            self.half_move_clock += 1
            if type(src_piece) == Pawn or tar_piece != self.empty_cell:
                self.half_move_clock = 0
            #####
            self.history.append({"src": src, "tar": tar, "src_piece": src_piece,
                                 "tar_piece": tar_piece, "castling": castling, "en_passant": en_passant,
                                 "en_passant_target_notation": self.en_passant_target_notation,
                                 "half_move": self.half_move_clock,
                                 "full_move": self.full_move_clock})
            self.board[tar_row][tar_col] = src_piece
            self.board[src_row][src_col] = self.empty_cell
            self.switch_side()
            return True
        return False

    def undo(self):
        pass

    def king_coordinate(self, color: Color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.get_color() == color and type(piece) == King:
                    return Coordinate(row, col)
        raise FileNotFoundError

    def check_win(self):
        pass

    def switch_side(self):
        if self.side == Color.WHITE:
            self.side = Color.BLACK
        else:
            self.side = Color.WHITE

    def get_side_notation(self):
        if self.side == Color.WHITE:
            return "w"
        return "b"

    def get_castling_notation(self):
        ret = ""
        king_move_w = True
        king_side_rook_move_w = True
        queen_side_rook_move_w = True
        king_move_b = True
        king_side_rook_move_b = True
        queen_side_rook_move_b = True
        for index in range(len(self.history)):
            if self.history[index]["src"].get_tuple() == (0, 4):
                king_move_w = False
            if self.history[index]["src"].get_tuple() == (0, 7):
                king_side_rook_move_w = False
            if self.history[index]["src"].get_tuple() == (0, 0):
                queen_side_rook_move_w = False
            if self.history[index]["src"].get_tuple() == (7, 4):
                king_move_b = False
            if self.history[index]["src"].get_tuple() == (7, 7):
                king_side_rook_move_b = False
            if self.history[index]["src"].get_tuple() == (7, 0):
                queen_side_rook_move_b = False
        if king_move_w & king_side_rook_move_w:
            ret += "K"
        if king_move_w & queen_side_rook_move_w:
            ret += "Q"
        if king_move_b & king_side_rook_move_b:
            ret += "k"
        if king_move_b & queen_side_rook_move_b:
            ret += "q"
        return ret

    def get_fen(self):
        ret = ""
        for row in range(7, -1, -1):
            count = 0
            for col in range(8):
                piece = self.board[row][col]
                if piece == self.empty_cell:
                    count += 1
                else:
                    if count != 0:
                        ret += str(count)
                        count = 0
                    ret += piece.to_string()
                if col == 7 and count > 0:
                    ret += str(count)
            if row > 0:
                ret += "/"
        ret += " "
        ret += self.get_side_notation()
        ret += " "
        ret += self.get_castling_notation()
        ret += " "
        ret += str(self.en_passant_target_notation)
        ret += " "
        ret += str(self.half_move_clock)
        ret += " "
        ret += str(self.full_move_clock)
        return ret

    def is_being_checked(self):
        king_coord = self.king_coordinate(self.side)
        for row in range(8):
            for col in range(8):
                if self.board[row][col].get_color() not in [self.side, Color.EMPTY]:
                    moves = self.board[row][col].get_moves()
                    if king_coord in moves:
                        return True
        return False

    def is_being_checked_after_move(self, src: Coordinate, tar: Coordinate) -> bool:
        src_row, src_col = src.get_tuple()
        tar_row, tar_col = tar.get_tuple()
        src_piece = self.board[src_row][src_col]
        tar_piece = self.board[tar_row][tar_col]
        self.board[tar_row][tar_col] = src_piece
        self.board[src_row][src_col] = self.empty_cell
        ret = self.is_being_checked()
        self.board[src_row][src_col] = src_piece
        self.board[tar_row][tar_col] = tar_piece
        return ret

    def get_piece_coordinate(self, piece: PieceInterface) -> Coordinate:
        for row in range(8):
            for col in range(8):
                if id(piece) == id(self.board[row][col]):
                    return Coordinate(row, col)
        raise FileNotFoundError

    def print_board(self):
        print()
        for row in range(7, -1, -1):
            print(Fore.LIGHTWHITE_EX + str(row), end=" ")
            for col in range(8):
                if self.board[row][col].get_color() == Color.BLACK:
                    print(Fore.BLACK + self.board[row][col].to_string(), end=" ")
                elif self.board[row][col].get_color() == Color.WHITE:
                    print(Fore.WHITE + self.board[row][col].to_string(), end=" ")
                else:
                    print(Fore.BLUE + self.board[row][col].to_string(), end=" ")
            print()
        print(" ", end=" ")
        for col in range(8):
            print(Fore.LIGHTWHITE_EX + str(col), end=" ")
        print()

        print(Style.RESET_ALL)
