from api.piece.utility import Utility
from api.piece.empty import Empty
from api.piece.pawn import Pawn
from api.piece.knight import Knight
from api.piece.bishop import Bishop
from api.piece.king import King
from api.piece.queen import Queen
from api.piece.rook import Rook
from api.piece.piece_interface import Color, PieceInterface


class ChessGame:
    """
    ChessGame is the workhorse of our app, it maintains the status of a ChessGame.
    """

    def __init__(self, fen="start"):
        """
        Initial game default values.
        :param fen: Fen string notation
        """
        self.board = []
        self.movement = []
        self.history = []
        self.fen = fen
        self.count = 1
        self.half_move_clock = 0
        self.full_move_clock = 1
        self.en_passant_target_notation = "-"
        self.castling_notation = "KQkq"
        self.passed_fen = fen
        self.empty_cell = Empty(None, Color.EMPTY, -1, -1)
        self.kings_coordinate = [None, None]
        self.piece_mapping = {
            "P": Pawn,
            "R": Rook,
            "N": Knight,
            "B": Bishop,
            "Q": Queen,
            "K": King}

        for row in range(8):
            row_list = []
            for col in range(8):
                row_list.append(self.empty_cell)
            self.board.append(row_list)
        self.turn = Color.WHITE

        self.load_fen(fen)

    def init_history(self, history: list) -> None:
        """
        Initial the game history.
        :param history: dict
        :return: None
        """
        if history:
            for ele in history:
                movement = {"src": ele[2],
                            "tar": ele[3]}
                fen = ele[4]
                self.history.append({"fen": fen, "movement": movement})
        return None

    def get_game_history(self) -> list:
        """
        Get game history array list with dictionary elements .
        :return: return the piece position movement history
        """
        ret = []
        if self.history:
            for ele in self.history:
                ret.append(ele["movement"])
        return ret

    def get_turn(self) -> str:
        """
        Get turn side color information.
        :return: A string which expresses the current turn side.
        """
        if self.turn == Color.WHITE:
            return "White"
        else:
            return "Black"

    def get_checked_moves(self, coordinate: tuple) -> dict:
        """
        While checkmate, each current turn piece available movements which can release the checkmate.
        :param coordinate: piece position
        :return: A dictionary with key "moves", and value is a array list which includes the available movements while
        checkmate.
        """
        row, col = coordinate
        piece = self.board[row][col]
        if piece.color != self.turn or self.check_game_status() != "Continue":
            return {"moves": []}
        ret = piece.get_checked_moves()["moves"]
        ret = Utility.encode_list(ret)
        return {"moves": ret}

    def update(self, src: tuple, tar: tuple, role: str, is_ai=False) -> bool:
        """
        Game parameter information will be updated after a valid movement and return True. If the movement is not valid,
        nothing will be updated, and return False.
        :param src: the position of the piece move from
        :param tar: the position of the piece move to
        :param role: promotion role while the pawn reaches the eighth rank to be replaced by.
        :param is_ai: promotion role while the pawn reaches the eighth rank to be replaced by.
        :return: A boolean value which show the movement is valid or not. If the movement is valid, all game parameters
        are updated, otherwise no change.
        """

        # If the game status is not 'Continue", then return False and nothing updated.
        if not is_ai and self.check_game_status() != "Continue":
            return False

        # If not in for the source piece turn, or the target movement position is not in the source piece movement list,
        # then then return False and nothing updated.
        src_row, src_col = src
        src_piece = self.board[src_row][src_col]
        if not is_ai and self.board[src_row][src_col].color != self.turn:
            return False
        if not is_ai and tar not in src_piece.get_checked_moves()["moves"]:
            return False

        tar_row, tar_col = tar
        tar_piece = self.board[tar_row][tar_col]

        # Implement en_passant
        if type(src_piece) == Pawn and src_col != tar_col and tar_piece == self.empty_cell:
            last_pawn_row, last_pawn_col = Utility.decode(self.history[-1]["movement"]["tar"])
            self.board[last_pawn_row][last_pawn_col] = self.empty_cell

        # Reset en_passant notation
        self.en_passant_target_notation = '-'

        # Update Rook and King firstMove.
        if type(src_piece) in [King, Rook]:
            src_piece.firstMove = False

        # Update castling notation
        self.castling_notation = self.get_castling_notation()

        # Update en_passant target square notation
        if type(src_piece) == Pawn:
            step = tar_row - src_row
            if abs(step) == 2 and src_col == tar_col:
                if step > 0:
                    self.en_passant_target_notation = Utility.encode(tar_row - 1, tar_col)
                else:
                    self.en_passant_target_notation = Utility.encode(tar_row + 1, tar_col)

        # Implement Castle
        if type(src_piece) == King and abs(src_col - tar_col) == 2:
            # Long castling
            if tar_col > src_col:
                rook = self.board[src_row][7]
                self.board[tar_row][tar_col - 1] = rook
                rook.update_coordinate(tar_row, tar_col - 1)
                self.board[src_row][7] = self.empty_cell
            # Short castling
            else:
                rook = self.board[src_row][0]
                self.board[tar_row][tar_col + 1] = rook
                rook.update_coordinate(tar_row, tar_col + 1)
                self.board[src_row][0] = self.empty_cell

        # Update movement clock counts
        self.count += 1
        if self.count % 2 == 0:
            self.full_move_clock += 1
        self.half_move_clock += 1
        if type(src_piece) == Pawn or type(tar_piece) != Empty:
            self.half_move_clock = 0

        # If the Pawn reached the button, then it would be promoted as promotion piece which passed through argument.
        if type(self.board[src_row][src_col]) == Pawn and tar_row in [0, 7]:
            color = self.board[src_row][src_col].color
            if role == "Rook":
                piece = Rook(self, color, tar_row, tar_row)
                piece.firstMove = False
            elif role == "Knight":
                piece = Knight(self, color, tar_row, tar_row)
            elif role == "Queen":
                piece = Queen(self, color, tar_row, tar_row)
            else:
                piece = Bishop(self, color, tar_row, tar_row)
            self.board[src_row][src_col] = self.empty_cell
            # noinspection PyTypeChecker
            self.board[tar_row][tar_col] = piece
            self.switch_turn()
        else:
            self.board[tar_row][tar_col] = src_piece
            src_piece.update_coordinate(tar_row, tar_col)
            self.board[src_row][src_col] = self.empty_cell
            if type(src_piece) == King:
                if self.turn == Color.WHITE:
                    self.kings_coordinate[0] = (tar_row, tar_col)
                else:
                    self.kings_coordinate[1] = (tar_row, tar_col)
            self.switch_turn()

        self.movement = {"src": Utility.encode(src_row, src_col), "tar": Utility.encode(tar_row, tar_col)}
        self.fen = self.get_fen()
        self.history.append({"fen": self.fen, "movement": self.movement})
        return True

    def undo(self) -> None:
        """
        Undo to the last step.
        :return: None
        """
        if len(self.history) > 0:
            del self.history[-1]

        if len(self.history) > 0:
            self.load_fen(self.history[-1]["fen"])
            self.fen = self.history[-1]["fen"]
        else:
            self.load_fen(self.passed_fen)
            self.fen = self.passed_fen
        return None

    def get_history(self) -> dict:
        """
        Get the game information after the last step movement.
        :return: A dictionary
        """
        if self.history:
            his = self.history[-1]
            step = len(self.history)
            fen = his["fen"]
            src = his["movement"]["src"]
            tar = his["movement"]["tar"]
            return {"src": src, "tar": tar, "fen": fen, "step": step}
        return {}

    def king_coordinate(self, color: Color) -> tuple:
        """
        Get the current turn side king position.
        :param color: the current turn colr
        :return: the position of the current turn side king
        """
        if color == Color.WHITE:
            return self.kings_coordinate[0]
        else:
            return self.kings_coordinate[1]

    def switch_turn(self) -> None:
        """
        After a valid movement, switch the current turn side color
        :return: None
        """
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE
        return None

    def get_turn_notation(self) -> str:
        """
        Get the turn side color notation, "b" expresses Black side, and "w" expresses white side.
        :return: turn notation string
        """
        if self.turn == Color.WHITE:
            return "w"
        return "b"

    def get_castling_notation(self) -> str:
        """
        A string which expresses which rooks are available for castling. If neither side can castle, this is
        "-". Otherwise, this has one or more letters: "K" (White can castle king_side), "Q" (White can castle
        queen_side), "k" (Black can castle king_side), and/or "q" (Black can castle queen_side). A move that
        temporarily prevents castling does not negate this notation.
        :return: str
        """
        ret = ""
        king_move_w = False
        king_side_rook_move_w = False
        queen_side_rook_move_w = False
        king_move_b = False
        king_side_rook_move_b = False
        queen_side_rook_move_b = False
        if type(self.board[0][4]) == King:
            king_move_w = self.board[0][4].firstMove
        if type(self.board[7][4]) == King:
            king_move_b = self.board[7][4].firstMove
        if type(self.board[0][0]) == Rook:
            queen_side_rook_move_w = self.board[0][0].firstMove
        if type(self.board[0][7]) == Rook:
            king_side_rook_move_w = self.board[0][7].firstMove
        if type(self.board[7][0]) == Rook:
            queen_side_rook_move_b = self.board[7][0].firstMove
        if type(self.board[7][7]) == Rook:
            king_side_rook_move_b = self.board[7][7].firstMove

        if king_move_w & king_side_rook_move_w:
            ret += "K"
        if king_move_w & queen_side_rook_move_w:
            ret += "Q"
        if king_move_b & king_side_rook_move_b:
            ret += "k"
        if king_move_b & queen_side_rook_move_b:
            ret += "q"
        if ret == "":
            ret = "-"
        return ret

    def get_fen(self) -> str:
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
                5. Halfmove clock: This is the number of half moves since the last capture or pawn advance. The reason
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

    def is_being_checked(self) -> bool:
        """
        To check the current turn side King is checked or not.
        :return: whether being checked
        """
        row, col = self.king_coordinate(self.turn)
        board = self.board
        # pawn
        if self.turn == Color.WHITE:
            ret_row = row + 1
        else:
            ret_row = row - 1
        for ret_col in [col + 1, col - 1]:
            if PieceInterface.is_valid_coord(ret_row, ret_col):
                piece = board[ret_row][ret_col]
                if piece.color not in [self.turn, Color.EMPTY] and type(piece) == Pawn:
                    return True
        # straight line
        dirs = [[1, 0],
                [0, 1],
                [-1, 0],
                [0, -1]]
        for direction in dirs:
            ret_row, ret_col = row + direction[0], col + direction[1]
            while PieceInterface.is_valid_coord(ret_row, ret_col):
                piece = board[ret_row][ret_col]
                tar_color = piece.color
                if tar_color != Color.EMPTY:
                    if tar_color != self.turn and (type(piece) == Queen or type(piece) == Rook):
                        return True
                    break
                ret_row += direction[0]
                ret_col += direction[1]
        # slash line
        dirs = [[1, 1],
                [-1, 1],
                [-1, -1],
                [1, -1]]
        for direction in dirs:
            ret_row, ret_col = row + direction[0], col + direction[1]
            while PieceInterface.is_valid_coord(ret_row, ret_col):
                piece = board[ret_row][ret_col]
                tar_color = piece.color
                if tar_color != Color.EMPTY:
                    if tar_color != self.turn and (type(piece) == Queen or type(piece) == Bishop):
                        return True
                    break
                ret_row += direction[0]
                ret_col += direction[1]

        dirs = [[2, 1],
                [1, 2],
                [-1, 2],
                [-2, 1],
                [-2, -1],
                [-1, -2],
                [1, -2],
                [2, -1]]
        for direction in dirs:
            ret_row, ret_col = row + direction[0], col + direction[1]
            if PieceInterface.is_valid_coord(ret_row, ret_col):
                piece = board[ret_row][ret_col]
                tar_color = piece.color
                if tar_color not in [Color.EMPTY, self.turn] and type(piece) == Knight:
                    return True
        dirs = [[1, 0],
                [1, 1],
                [1, -1],
                [0, 1],
                [0, -1],
                [-1, 1],
                [-1, 0],
                [-1, -1]]
        for direction in dirs:
            ret_row, ret_col = row + direction[0], col + direction[1]
            if PieceInterface.is_valid_coord(ret_row, ret_col):
                piece = board[ret_row][ret_col]
                tar_color = piece.color
                if tar_color not in [Color.EMPTY, self.turn] and type(piece) == King:
                    return True

        return False

    def is_being_checked_after_move(self, src: tuple, tar: tuple) -> bool:
        """
        A boolean value which expresses after this piece movement, the current king is still checked or not
        :param src: the position of a piece move from
        :param tar: the position of a piece move to
        :return: whether being checked if update from src to tar
        """
        src_row, src_col = src
        tar_row, tar_col = tar
        src_piece = self.board[src_row][src_col]
        tar_piece = self.board[tar_row][tar_col]
        self.board[tar_row][tar_col] = src_piece
        src_piece.update_coordinate(tar_row, tar_col)
        if type(src_piece) == King:
            if self.turn == Color.WHITE:
                self.kings_coordinate[0] = (tar_row, tar_col)
            else:
                self.kings_coordinate[1] = (tar_row, tar_col)
        self.board[src_row][src_col] = self.empty_cell
        ret = self.is_being_checked()
        self.board[src_row][src_col] = src_piece
        self.board[tar_row][tar_col] = tar_piece
        src_piece.update_coordinate(src_row, src_col)
        if type(src_piece) == King:
            if self.turn == Color.WHITE:
                self.kings_coordinate[0] = (src_row, src_col)
            else:
                self.kings_coordinate[1] = (src_row, src_col)
        return ret

    def check_game_status(self) -> str:
        """
        During the game procedure, check the current game status to judge game ending or continuing.
        return the current turn game status. "Continue" expresses the game could be continued. "Draw" expresses
        draw and game ending, or "WhiteLoss"/"BlackLoss" expresses which color side lose the game and game
        ending.
        :return: Game status which including Continue, Draw, BlackLoss, WhiteLoss
        """

        # If keeping move neither Pawn or Capture for 50 half steps, the game would be ended as "Draw"
        if self.half_move_clock == 50:
            return "Draw"

        # Not in check status, if the turn side is Stalemate, the game would be ended as "Draw", otherwise "Continue".
        if not self.is_being_checked():
            for row in range(8):
                for col in range(8):
                    if self.board[row][col].color == self.turn:
                        moves = self.board[row][col].get_moves()
                        for tar in moves:
                            if not self.is_being_checked_after_move((row, col), tar):
                                return "Continue"
            return "Draw"

        # In check status, if the turn side could not release the check status, the game would be ended as the current
        # turn side "Loss", otherwise "Continue".
        if self.is_being_checked():
            for row in range(8):
                for col in range(8):
                    if self.board[row][col].color == self.turn:
                        moves = self.board[row][col].get_checked_moves()["moves"]
                        if len(moves) > 0:
                            return "Continue"
            if self.turn == Color.WHITE:
                return "WhiteLoss"
            else:
                return "BlackLoss"

    def load_fen(self, fen_str: str) -> None:
        """
        Based on the provided fen, recover the game board and game character values.
        :param fen_str: A fen string which should be under fen standard
        :return: None
        """
        if fen_str == "start":
            fen_str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
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
        self.castling_notation = field[2]

        while fen_str[index] != " ":
            if fen_str[index] == "/":
                row -= 1
                col = 0
            elif fen_str[index].isnumeric():
                for i in range(int(fen_str[index])):
                    self.board[row][col] = self.empty_cell
                    col += 1
            else:
                piece = self.to_piece(fen_str[index], row, col)
                if fen_str[index] == "K":
                    self.kings_coordinate[0] = (row, col)
                elif fen_str[index] == "k":
                    self.kings_coordinate[1] = (row, col)
                elif fen_str[index] == "R":
                    if (col != 0 and col != 7) or row != 0:
                        piece.firstMove = False
                    elif col == 0 and "Q" not in self.castling_notation:
                        piece.firstMove = False
                    elif col == 7 and "K" not in self.castling_notation:
                        piece.firstMove = False
                if fen_str[index] == "r":
                    if (col != 0 and col != 7) or row != 7:
                        piece.firstMove = False
                    elif col == 0 and "q" not in self.castling_notation:
                        piece.firstMove = False
                    elif col == 7 and "k" not in self.castling_notation:
                        piece.firstMove = False

                # noinspection PyTypeChecker
                self.board[row][col] = piece
                col += 1
            index += 1
        return None

    def to_piece(self, char: str, x: int, y: int) -> PieceInterface:
        """
        Get the piece from the given char.
        :param char: A char among (P N B R Q K p n b r q k)
        :param x:
        :param y:
        :return: A piece
        """
        if char == "*":
            return self.empty_cell

        if char.islower():
            color = Color.BLACK
        else:
            color = Color.WHITE
        return self.piece_mapping[char.upper()](self, color, x, y)

    def print_board(self) -> None:
        """
        Print the game board for the front end using.
        :return: None
        """
        print()
        for row in range(7, -1, -1):
            print(str(row), end=" ")
            for col in range(8):
                if self.board[row][col].color == Color.BLACK:
                    print(self.board[row][col].to_string(), end=" ")
                elif self.board[row][col].color == Color.WHITE:
                    print(self.board[row][col].to_string(), end=" ")
                else:
                    print(self.board[row][col].to_string(), end=" ")
            print()
        print(" ", end=" ")
        for col in range(8):
            print(str(col), end=" ")
        print()
        return None
