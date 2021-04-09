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
import re


class ChessGame:
    def __init__(self, fen="start"):
        """
        Initial game default values.
        :param fen:
        """
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
        self.turn = Color.WHITE

        if fen == "start":
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.load_fen(fen)

    def init_history(self, history):
        """
        :param history:
        :return:
        """
        for ele in history:
            src = ele["src"]
            row, col = tuple(map(int, re.findall(r'[0-9]+', src)))
            src = Coordinate(row, col)
            tar = ele["tar"]
            row, col = tuple(map(int, re.findall(r'[0-9]+', tar)))
            tar = Coordinate(row, col)
            # no use rn
            src_piece = self.empty_cell
            tar_piece = self.empty_cell
            castling = ele["castling"]
            en_passant = ele["en_passant"]
            en_passant_target_notation = ele["en_passant_target_notation"]
            half_move_clock = ele["half_move"]
            full_move_clock = ele["full_move"]
            self.history.append({"src": src, "tar": tar, "src_piece": src_piece,
                                 "tar_piece": tar_piece, "castling": castling, "en_passant": en_passant,
                                 "en_passant_target_notation": en_passant_target_notation,
                                 "half_move": half_move_clock,
                                 "full_move": full_move_clock})

    def get_game_history(self):
        """

        :return: return the piece position movement history
        """
        ret = []
        for ele in self.history:
            ret.append({"src": Coordinate.encode(ele["src"]), "tar": Coordinate.encode(ele["tar"])})
        return ret

    def get_turn(self) -> str:
        """

        :return: the current turn
        """
        if self.turn == Color.WHITE:
            return "White"
        else:
            return "Black"

    def get_checked_moves(self, coordinate: Coordinate) -> dict:
        """
        While checkmate, each current turn piece available movements which can release the checkmate.
        :param coordinate: piece position
        :return: possible movements while checkmate
        """
        row, col = coordinate.get_tuple()
        piece = self.board[row][col]
        if piece.get_color() != self.turn or self.check_game_status() != "Continue":
            return {"moves": []}
        ret = piece.get_checked_moves()["moves"]
        ret = Coordinate.encode_list(ret)
        return {"moves": ret}

    def update(self, src: Coordinate, tar: Coordinate, role: str) -> bool:
        """

        :param src: the position of the piece move from
        :param tar: the position of the piece move to
        :param role: promotion role while the pawn reaches the eighth rank to be replaced by.
        :return: A boolean value which show the movement is valid or not. If the movement is valid, all game parameters
                 are updated, otherwise no change.
        """
        src_row, src_col = src.get_tuple()
        src_piece = self.board[src_row][src_col]
        if self.check_game_status() == "Continue" and self.board[src_row][src_col].get_color() == self.turn and \
                tar in src_piece.get_checked_moves()["moves"]:
            tar_row, tar_col = tar.get_tuple()
            tar_piece = self.board[tar_row][tar_col]
            castling = False
            en_passant = False
            self.en_passant_target_notation = "-"
            if type(src_piece) in [King, Rook]:
                src_piece.firstMove = False
            # add trace for en_passant target square notation
            if type(src_piece) == Pawn:
                step = tar_row - src_row
                if abs(step) == 2 and src_col == tar_col:
                    if step > 0:
                        self.en_passant_target_notation = Coordinate(tar_row - 1, tar_col).encode()
                    else:
                        self.en_passant_target_notation = Coordinate(tar_row + 1, tar_col).encode()
            # update the En passant
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
            # update the movement counts
            self.count += 1
            if self.count % 2 == 0:
                self.full_move_clock += 1

            self.half_move_clock += 1
            if type(src_piece) == Pawn or type(tar_piece) != Empty:
                self.half_move_clock = 0
            # update the game history
            self.history.append({"src": src, "tar": tar, "src_piece": src_piece,
                                 "tar_piece": tar_piece, "castling": castling, "en_passant": en_passant,
                                 "en_passant_target_notation": self.en_passant_target_notation,
                                 "half_move": self.half_move_clock,
                                 "full_move": self.full_move_clock})

            if type(self.board[src_row][src_col]) == Pawn and tar_row in [0, 7]:
                color = self.board[src_row][src_col].get_color()
                if role == "Rook":
                    piece = Rook(self, color)
                    piece.firstMove = False
                elif role == "Knight":
                    piece = Knight(self, color)
                elif role == "Queen":
                    piece = Queen(self, color)
                else:
                    piece = Bishop(self, color)
                self.board[src_row][src_col] = self.empty_cell
                self.board[tar_row][tar_col] = piece
                self.switch_turn()
            else:
                self.board[tar_row][tar_col] = src_piece
                self.board[src_row][src_col] = self.empty_cell
                self.switch_turn()
            return True
        return False

    def undo(self):
        """
        Sprint2 misssion
        :return:
        """
        pass

    def get_history(self):
        """

        :return: A dictionary record the game status after the last movement which are used by the front end.
        """
        if self.history:
            his = self.history[-1]
            step = len(self.history)
            src = str(his["src"])
            tar = str(his["tar"])
            half_move = his["half_move"]
            full_move = his["full_move"]
            en_passant_target_notation = his["en_passant_target_notation"]
            return {"src": src, "tar": tar, "castling": his["castling"], "en_passant": his["en_passant"],
                    "en_passant_target_notation": en_passant_target_notation,
                    "half_move": half_move,
                    "full_move": full_move, "step": step}
        return {}

    def king_coordinate(self, color: Color):
        """

        :param color: the current turn colr
        :return: the position of the current turn side king
        """
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.get_color() == color and type(piece) == King:
                    return Coordinate(row, col)
        raise FileNotFoundError

    def switch_turn(self):
        """
        After a valid movement, switch the current turn side color
        :return: void
        """
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE

    def get_turn_notation(self):
        """

        :return: the current turn side color, "b" expresses Black side, and "w" expresses white side
        """
        if self.turn == Color.WHITE:
            return "w"
        return "b"

    def get_castling_notation(self):
        """

        :return: A string which expresses which rooks are available for castling. If neither side can castle, this is
                "-". Otherwise, this has one or more letters: "K" (White can castle king_side), "Q" (White can castle
                queen_side), "k" (Black can castle king_side), and/or "q" (Black can castle queen_side). A move that
                temporarily prevents castling does not negate this notation.
        """
        ret = ""
        king_move_w = True
        king_turn_rook_move_w = True
        queen_turn_rook_move_w = True
        king_move_b = True
        king_turn_rook_move_b = True
        queen_turn_rook_move_b = True
        if len(self.history) == 0:
            return "KQkq"
        for index in range(len(self.history)):
            if self.history[index]["src"].get_tuple() == (0, 4):
                king_move_w = False
            if self.history[index]["src"].get_tuple() == (0, 7):
                king_turn_rook_move_w = False
            if self.history[index]["src"].get_tuple() == (0, 0):
                queen_turn_rook_move_w = False
            if self.history[index]["src"].get_tuple() == (7, 4):
                king_move_b = False
            if self.history[index]["src"].get_tuple() == (7, 7):
                king_turn_rook_move_b = False
            if self.history[index]["src"].get_tuple() == (7, 0):
                queen_turn_rook_move_b = False
        if king_move_w & king_turn_rook_move_w:
            ret += "K"
        if king_move_w & queen_turn_rook_move_w:
            ret += "Q"
        if king_move_b & king_turn_rook_move_b:
            ret += "k"
        if king_move_b & queen_turn_rook_move_b:
            ret += "q"
        if ret == "":
            ret = "-"
        return ret

    def get_fen(self):
        """
        A FEN is a standard notation for describing a particular board position of a chess game. The purpose of FEN is
        to provide all the necessary information to restart a game from a particular position.
        :return: A string which contains six fields. The separator between fields is a space. The fields are:
                1. Piece placement (from White's perspective). Each rank is described, starting with rank 8 and ending
                   with rank 1; within each rank, the contents of each square are described from file "a" through file
                   "h". Following the Standard Algebraic Notation (SAN), each piece is identified by a single letter
                   taken from the standard English names (pawn = "P", knight = "N", bishop = "B", rook = "R",
                   queen = "Q" and king = "K"). White pieces are designated using upper-case letters ("PNBRQK")
                   while black pieces use lowercase ("pnbrqk"). Empty squares are noted using digits 1 through 8
                   (the number of empty squares), and "/" separates ranks.
                2. Active color. "w" means White moves next, "b" means Black moves next.
                3. Castling availability. If neither side can castle, this is "-". Otherwise, this has one or more
                   letters: "K" (White can castle kingside), "Q" (White can castle queenside), "k" (Black can castle
                   kingside), and/or "q" (Black can castle queenside). A move that temporarily prevents castling does
                   not negate this notation.
                4. En passant target square in algebraic notation. If there's no en passant target square, this is "-".
                   If a pawn has just made a two-square move, this is the position "behind" the pawn. This is recorded
                   regardless of whether there is a pawn in position to make an en passant capture.
                5. Halfmove clock: This is the number of halfmoves since the last capture or pawn advance. The reason
                   for this field is that the value is used in the fifty-move rule.
                6. Fullmove number: The number of the full move. It starts at 1, and is incremented after Black's move.
        """
        ret = ""
        for row in range(7, -1, -1):
            count = 0
            for col in range(8):
                piece = self.board[row][col]
                if type(piece) == Empty:
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
        ret += self.get_turn_notation()
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
        """

        :return: A boolean value which expresses the current turn kind is checked or not.
        """
        king_coord = self.king_coordinate(self.turn)
        for row in range(8):
            for col in range(8):
                if self.board[row][col].get_color() not in [self.turn, Color.EMPTY]:
                    moves = self.board[row][col].get_moves()
                    if king_coord in moves:
                        return True
        return False

    def is_being_checked_after_move(self, src: Coordinate, tar: Coordinate) -> bool:
        """

        :param src: the position of a piece move from
        :param tar: the position of a piece move to
        :return: A boolean value which expresses after this piece movement, the current king is still checked or not
        """
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

    def check_game_status(self):
        """
        During the game procedure, check the current game status to judge game ending or continuing.
        :return: return the current turn game status. "Continue" expresses the game could be continued. "Draw" expresses
                 draw and game ending, or "WhiteLoss"/"BlackLoss" expresses which color side lose the game and game
                 ending.
        """
        if self.half_move_clock == 50:
            return "Draw"
        if not self.is_being_checked():
            for row in range(8):
                for col in range(8):
                    if self.board[row][col].get_color() == self.turn:
                        moves = self.board[row][col].get_moves()
                        for tar in moves:
                            if not self.is_being_checked_after_move(Coordinate(row, col), tar):
                                return "Continue"
            return "Draw"
        if self.is_being_checked():
            for row in range(8):
                for col in range(8):
                    if self.board[row][col].get_color() == self.turn:
                        moves = self.board[row][col].get_checked_moves()["moves"]
                        if len(moves) > 0:
                            return "Continue"
            if self.turn == Color.WHITE:
                return "WhiteLoss"
            else:
                return "BlackLoss"

    def get_piece_coordinate(self, piece: PieceInterface) -> Coordinate:
        """

         :param piece: a piece
         :return: the position of the piece
         """
        for row in range(8):
            for col in range(8):
                if id(piece) == id(self.board[row][col]):
                    return Coordinate(row, col)
        raise FileNotFoundError

    def print_board(self):
        """
        Print the game board for the front end using.
        :return:
        """
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

    def load_fen(self, fen_str):
        """
        Based on the provided fen, recover the game board and game character values.
        :param fen_str: A fen string which should be under fen standard
        :return: void
        """
        index, row, col = 0, 7, 0
        field = fen_str.split()

        if field[1] == "w":
            self.turn = Color.WHITE
        else:
            self.turn = Color.BLACK

        self.en_passant_target_notation = field[3]
        self.half_move_clock = int(field[4])
        self.full_move_clock = int(field[5])
        self.count = (int(field[5]) - 1) * 2 + (self.turn == Color.BLACK)
        castling = field[2]

        while fen_str[index] != " ":
            if fen_str[index] == "/":
                row -= 1
                col = 0
            elif fen_str[index].isnumeric():
                for i in range(int(fen_str[index])):
                    self.board[row][col] = self.empty_cell
                    col += 1
            else:
                piece = self.to_piece(fen_str[index])
                if fen_str[index] == "R":
                    if (col != 0 and col != 7) or row != 0:
                        piece.firstMove = False
                    elif col == 0 and "Q" not in castling:
                        piece.firstMove = False
                    elif col == 7 and "K" not in castling:
                        piece.firstMove = False
                if fen_str[index] == "r":
                    if (col != 0 and col != 7) or row != 7:
                        piece.firstMove = False
                    elif col == 0 and "q" not in castling:
                        piece.firstMove = False
                    elif col == 7 and "k" not in castling:
                        piece.firstMove = False

                self.board[row][col] = piece
                col += 1
            index += 1

    def to_piece(self, char):
        """

        :param char: A char among (P N B R Q K p n b r q k)
        :return: Piece interface
        """
        p = Empty(None, Color.EMPTY)
        if char == "P":
            p = Pawn(self, Color.WHITE)
        if char == "N":
            p = Knight(self, Color.WHITE)
        if char == "B":
            p = Bishop(self, Color.WHITE)
        if char == "R":
            p = Rook(self, Color.WHITE)
        if char == "Q":
            p = Queen(self, Color.WHITE)
        if char == "K":
            p = King(self, Color.WHITE)
        if char == "p":
            p = Pawn(self, Color.BLACK)
        if char == "n":
            p = Knight(self, Color.BLACK)
        if char == "b":
            p = Bishop(self, Color.BLACK)
        if char == "r":
            p = Rook(self, Color.BLACK)
        if char == "q":
            p = Queen(self, Color.BLACK)
        if char == "k":
            p = King(self, Color.BLACK)
        return p
