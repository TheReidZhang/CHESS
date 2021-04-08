import unittest
from chess.chess_game import ChessGame
from chess.piece.pawn import Pawn
from chess.piece.knight import Knight
from chess.piece.bishop import Bishop
from chess.piece.king import King
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.piece.empty import Empty
from chess.piece.piece_interface import Color
from chess.piece.coordinate import Coordinate
import random


class TestInitial(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_initial_start(self):
        self.assertEqual(self.game.turn, Color.WHITE)
        self.assertEqual(type(self.game.empty_cell), Empty)
        self.assertEqual(self.game.history, [])
        self.assertEqual(self.game.count, 0)
        self.assertEqual(self.game.half_move_clock, 0)
        self.assertEqual(self.game.full_move_clock, 1)
        self.assertEqual(self.game.en_passant_target_notation, "-")
        for col in range(8):
            self.game.board[1][col] = Pawn(self.game, Color.WHITE)
            self.game.board[6][col] = Pawn(self.game, Color.BLACK)
        for row, color in [(0, Color.WHITE), (7, Color.BLACK)]:
            self.game.board[row][0] = Rook(self.game, color)
            self.game.board[row][7] = Rook(self.game, color)
            self.game.board[row][1] = Knight(self.game, color)
            self.game.board[row][6] = Knight(self.game, color)
            self.game.board[row][2] = Bishop(self.game, color)
            self.game.board[row][5] = Bishop(self.game, color)
            self.game.board[row][3] = Queen(self.game, color)
            self.game.board[row][4] = King(self.game, color)


class TestGetTurn(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_get_turn_start(self):
        self.assertEqual(self.game.get_turn(), "White")

    def test_switch_turn_during_game(self):
        self.game.turn = Color.BLACK
        self.assertEqual(self.game.get_turn(), "Black")

        self.game.turn = Color.WHITE
        self.assertEqual(self.game.get_turn(), "White")


class TestGetCheckedMoves(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")
        self.game.half_move_clock = 20
        self.game.full_move_clock = 100
        self.game.count = 200
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)

    def test_get_checked_moves_checkmate(self):
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][4] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK)
        self.game.turn = Color.WHITE

        checked_moves = self.game.get_checked_moves(Coordinate(4, 1))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in ["b2"])

        checked_moves = self.game.get_checked_moves(Coordinate(0, 0))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in ["a2"])

        checked_moves = self.game.get_checked_moves(Coordinate(4, 5))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in [])

    def test_get_checked_moves_checkmate2(self):
        self.game.board[0][3] = King(self.game, Color.WHITE)
        self.game.board[7][4] = King(self.game, Color.BLACK)
        self.game.board[1][2] = Pawn(self.game, Color.BLACK)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[3][4] = Bishop(self.game, Color.BLACK)
        self.game.turn = Color.WHITE

        checked_moves = self.game.get_checked_moves(Coordinate(0, 3))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in ["c1", "d2", "e1", "e2"])

        checked_moves = self.game.get_checked_moves(Coordinate(4, 1))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in [])


class TestUpDate(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_update_start_move_black(self):
        random_num_1 = random.randint(0, 7)
        random_num_2 = random.randint(0, 7)
        for row in range(6, 8):
            for col in range(8):
                self.assertFalse(self.game.update(Coordinate(row, col),
                                                  Coordinate(random_num_1, random_num_2), "Queen"))

    def test_update_move_pawn(self):
        for col in range(8):
            self.assertTrue(self.game.update(Coordinate(1, col), Coordinate(3, col), "Queen"))
            self.assertEqual(self.game.en_passant_target_notation, chr(ord('a') + col) + "3")
            self.game.turn = Color.WHITE
        for col in range(8):
            self.assertTrue(self.game.update(Coordinate(3, col), Coordinate(4, col), "Queen"))
            self.game.turn = Color.WHITE

    def test_update_move_white(self):
        random_num_1 = random.randint(0, 7)
        random_num_2 = random.randint(0, 7)
        self.assertFalse(self.game.update(Coordinate(0, 0), Coordinate(random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.update(Coordinate(0, 1), Coordinate(2, 0), "Queen"))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.update(Coordinate(2, 0), Coordinate(0, 1), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update(Coordinate(0, 2), Coordinate(random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update(Coordinate(0, 3), Coordinate(random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update(Coordinate(0, 4), Coordinate(random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update(Coordinate(0, 5), Coordinate(random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.update(Coordinate(0, 6), Coordinate(2, 7), "Queen"))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.update(Coordinate(2, 7), Coordinate(0, 6), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update(Coordinate(0, 7), Coordinate(random_num_1, random_num_2), "Queen"))

    def test_update_history(self):
        self.game.update(Coordinate(1, 0), Coordinate(3, 0), "Queen")
        self.assertEqual(self.game.history[0]["src"], Coordinate(1, 0))
        self.assertEqual(self.game.history[0]["tar"], Coordinate(3, 0))
        self.assertEqual(type(self.game.history[0]["src_piece"]), Pawn)
        self.assertEqual(type(self.game.history[0]["tar_piece"]), Empty)
        self.assertEqual(self.game.history[0]["castling"], False)
        self.assertEqual(self.game.history[0]["en_passant"], False)
        self.assertEqual(self.game.history[0]["en_passant_target_notation"], "a3")
        self.assertEqual(self.game.history[0]["half_move"], 0)
        self.assertEqual(self.game.history[0]["full_move"], 1)


class TestGetHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_get_history_start(self):
        self.assertEqual(self.game.get_history(), {})

    def test_get_history_during_game(self):
        self.game.history = [{"src": Coordinate(1, 0), "tar": Coordinate(2, 0),
                              "src_piece": Pawn(self.game, Color.WHITE),
                              "tar_piece": Empty(None, Color.EMPTY),
                              "castling": False, "en_passant": False,
                              "en_passant_target_notation": "-",
                              "half_move": 0, "full_move": 1}]
        expect = {"src": "(1,0)", "tar": "(2,0)", "castling": False,
                  "en_passant": False, "en_passant_target_notation": "-",
                  "half_move": 0, "full_move": 1, "step": 1}
        self.assertEqual(self.game.get_history(), expect)

        self.game.history = [{"src": Coordinate(1, 0), "tar": Coordinate(2, 0),
                              "src_piece": Pawn(self.game, Color.WHITE),
                              "tar_piece": Empty(None, Color.EMPTY),
                              "castling": False, "en_passant": False,
                              "en_passant_target_notation": "-",
                              "half_move": 0, "full_move": 1},
                             {"src": Coordinate(6, 0), "tar": Coordinate(4, 0),
                              "src_piece": Pawn(self.game, Color.BLACK),
                              "tar_piece": Empty(None, Color.EMPTY),
                              "castling": False, "en_passant": False,
                              "en_passant_target_notation": "a6",
                              "half_move": 0, "full_move": 1}]
        expect = {"src": "(6,0)", "tar": "(4,0)",
                  "castling": False,
                  "en_passant": False, "en_passant_target_notation": "a6",
                  "half_move": 0, "full_move": 1, "step": 2}
        self.assertEqual(self.game.get_history(), expect)


class TestKingCoordinate(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_king_coordinate_start(self):
        self.assertEqual(self.game.king_coordinate(Color.WHITE), Coordinate(0, 4))
        self.assertEqual(self.game.king_coordinate(Color.BLACK), Coordinate(7, 4))

    def test_king_coordinate(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK)
        self.assertEqual(self.game.king_coordinate(Color.WHITE), Coordinate(0, 0))
        self.assertEqual(self.game.king_coordinate(Color.BLACK), Coordinate(7, 3))


class TestSwitchTurn(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_switch_turn_start(self):
        self.game.switch_turn()
        self.assertEqual(self.game.turn, Color.BLACK)

    def test_switch_turn_during_game(self):
        self.game.turn = Color.BLACK
        self.game.switch_turn()
        self.assertEqual(self.game.turn, Color.WHITE)
        self.game.switch_turn()
        self.assertEqual(self.game.turn, Color.BLACK)


class TestGetTurnNotation(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_get_turn_notation_start(self):
        self.assertEqual(self.game.get_turn_notation(), "w")

    def test_get_turn_notation_during_game(self):
        self.game.turn = Color.BLACK
        self.assertEqual(self.game.get_turn_notation(), "b")
        self.game.turn = Color.WHITE
        self.assertEqual(self.game.get_turn_notation(), "w")


class TestGetCastlingNotation(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_get_castling_notation_start(self):
        self.assertEqual(self.game.get_castling_notation(), "KQkq")

    def test_get_castling_notation_during_game(self):
        self.game.history = [{"src": Coordinate(0, 0)}]
        self.assertEqual(self.game.get_castling_notation(), "Kkq")

        self.game.history = [{"src": Coordinate(0, 7)}]
        self.assertEqual(self.game.get_castling_notation(), "Qkq")

        self.game.history = [{"src": Coordinate(0, 0)}, {"src": Coordinate(0, 7)}]
        self.assertEqual(self.game.get_castling_notation(), "kq")

        self.game.history = [{"src": Coordinate(0, 4)}]
        self.assertEqual(self.game.get_castling_notation(), "kq")

        self.game.history = [{"src": Coordinate(7, 4)}]
        self.assertEqual(self.game.get_castling_notation(), "KQ")

        self.game.history = [{"src": Coordinate(7, 0)}]
        self.assertEqual(self.game.get_castling_notation(), "KQk")

        self.game.history = [{"src": Coordinate(7, 7)}]
        self.assertEqual(self.game.get_castling_notation(), "KQq")

        self.game.history = [{"src": Coordinate(7, 0)}, {"src": Coordinate(7, 7)}]
        self.assertEqual(self.game.get_castling_notation(), "KQ")

        self.game.history = [{"src": Coordinate(0, 7)},
                             {"src": Coordinate(7, 0)}, {"src": Coordinate(7, 7)}]
        self.assertEqual(self.game.get_castling_notation(), "Q")

        self.game.history = [{"src": Coordinate(0, 0)},
                             {"src": Coordinate(7, 0)}, {"src": Coordinate(7, 7)}]
        self.assertEqual(self.game.get_castling_notation(), "K")

        self.game.history = [{"src": Coordinate(0, 0)}, {"src": Coordinate(0, 7)},
                             {"src": Coordinate(7, 7)}]
        self.assertEqual(self.game.get_castling_notation(), "q")

        self.game.history = [{"src": Coordinate(0, 0)}, {"src": Coordinate(0, 7)},
                             {"src": Coordinate(7, 0)}]
        self.assertEqual(self.game.get_castling_notation(), "k")

        self.game.history = [{"src": Coordinate(0, 0)}, {"src": Coordinate(0, 7)},
                             {"src": Coordinate(7, 0)}, {"src": Coordinate(7, 7)}]
        self.assertEqual(self.game.get_castling_notation(), "-")

        self.game.history = [{"src": Coordinate(0, 4)}, {"src": Coordinate(7, 4)}]
        self.assertEqual(self.game.get_castling_notation(), "-")


class TestGetFen(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_get_fen_start(self):
        self.assertEqual(self.game.get_fen(),
                         "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_get_fen_in_few_moves(self):
        self.game.update(Coordinate(1, 4), Coordinate(3, 4), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        self.game.update(Coordinate(6, 2), Coordinate(4, 2), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
        self.game.update(Coordinate(0, 6), Coordinate(2, 5), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
        self.game.update(Coordinate(6, 0), Coordinate(4, 0), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "rnbqkbnr/1p1ppppp/8/p1p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq a6 0 3")
        self.game.update(Coordinate(0, 7), Coordinate(0, 6), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "rnbqkbnr/1p1ppppp/8/p1p5/4P3/5N2/PPPP1PPP/RNBQKBR1 b Qkq - 1 3")
        self.game.update(Coordinate(7, 0), Coordinate(6, 0), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "1nbqkbnr/rp1ppppp/8/p1p5/4P3/5N2/PPPP1PPP/RNBQKBR1 w Qk - 2 4")
        self.game.update(Coordinate(1, 0), Coordinate(3, 0), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "1nbqkbnr/rp1ppppp/8/p1p5/P3P3/5N2/1PPP1PPP/RNBQKBR1 b Qk a3 0 4")
        self.game.update(Coordinate(6, 7), Coordinate(4, 7), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "1nbqkbnr/rp1pppp1/8/p1p4p/P3P3/5N2/1PPP1PPP/RNBQKBR1 w Qk h6 0 5")
        self.game.update(Coordinate(0, 0), Coordinate(1, 0), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "1nbqkbnr/rp1pppp1/8/p1p4p/P3P3/5N2/RPPP1PPP/1NBQKBR1 b k - 1 5")
        self.game.update(Coordinate(7, 7), Coordinate(6, 7), "Queen")
        self.assertEqual(self.game.get_fen(),
                         "1nbqkbn1/rp1ppppr/8/p1p4p/P3P3/5N2/RPPP1PPP/1NBQKBR1 w - - 2 6")

    def test_get_fen_during_game(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK)
        self.game.history = [{"src": Coordinate(0, 4)}, {"src": Coordinate(7, 4)}]
        self.game.en_passant_target_notation = "-"
        self.game.half_move_clock = 0
        self.game.full_move_clock = 20
        self.assertEqual(self.game.get_fen(),
                         "3k4/8/8/1R3P2/3b4/8/p7/K7 w - - 0 20")


class TestIsBeingChecked(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_is_being_checked_start(self):
        self.assertFalse(self.game.is_being_checked())

    def test_is_being_checked_during_game_true(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK)
        self.assertTrue(self.game.is_being_checked())

    def test_is_being_checked_during_game_false(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][4] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK)
        self.assertFalse(self.game.is_being_checked())


class TestIsBeingCheckedAfterMove(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_is_being_checked_after_move_start(self):
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(1, 4), Coordinate(3, 4)))

    def test_is_being_checked_after_move_in_few_moves(self):
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(6, 2), Coordinate(4, 2)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(0, 6), Coordinate(2, 5)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(0, 6), Coordinate(2, 5)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(6, 0), Coordinate(4, 0)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(0, 7), Coordinate(0, 6)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(7, 0), Coordinate(6, 0)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(1, 0), Coordinate(3, 0)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(6, 7), Coordinate(4, 7)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(0, 0), Coordinate(1, 0)))
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(7, 7), Coordinate(6, 7)))

    def test_is_being_checked_after_move_during_game_true(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[4][2] = Bishop(self.game, Color.BLACK)
        self.assertTrue(self.game.is_being_checked_after_move(Coordinate(4, 2), Coordinate(3, 3)))

    def test_is_being_checked_after_move_during_game_false(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][4] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[4][2] = Bishop(self.game, Color.BLACK)
        self.assertFalse(self.game.is_being_checked_after_move(Coordinate(4, 2), Coordinate(2, 4)))


class TestCheckGameStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_check_game_status_start(self):
        self.assertEqual(self.game.check_game_status(), "Continue")

    def test_check_game_status_half_move_draw(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[3][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[2][0] = Bishop(self.game, Color.BLACK)
        self.game.board[2][1] = Bishop(self.game, Color.BLACK)
        self.game.half_move_clock = 50
        self.assertEqual(self.game.check_game_status(), "Draw")

    def test_check_game_status_without_check_draw(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[2][0] = Bishop(self.game, Color.BLACK)
        self.game.board[2][1] = Bishop(self.game, Color.BLACK)
        self.assertEqual(self.game.check_game_status(), "Draw")

    def test_check_game_status_without_check_continue(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[2][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[2][0] = Bishop(self.game, Color.BLACK)
        self.assertEqual(self.game.check_game_status(), "Continue")

    def test_check_game_status_with_check_continue(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK)
        self.assertEqual(self.game.check_game_status(), "Continue")

    def test_check_game_status_with_check_loss(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[3][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[2][2] = Bishop(self.game, Color.BLACK)
        self.game.board[2][1] = Bishop(self.game, Color.BLACK)
        self.assertEqual(self.game.check_game_status(), "WhiteLoss")


class TestPieceCoordinate(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_piece_coordinate_start(self):
        for row in range(2):
            for col in range(8):
                self.assertEqual(self.game.get_piece_coordinate(self.game.board[0][col]), Coordinate(0, col))
        for row in range(6, 8):
            for col in range(8):
                self.assertEqual(self.game.get_piece_coordinate(self.game.board[0][col]), Coordinate(0, col))

    def test__piece_coordinate_during_game(self):
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = Empty(None, Color.EMPTY)
        self.game.board[0][0] = King(self.game, Color.WHITE)
        self.game.board[7][3] = King(self.game, Color.BLACK)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK)
        self.game.board[3][5] = Pawn(self.game, Color.WHITE)
        self.game.board[4][1] = Rook(self.game, Color.WHITE)
        self.game.board[2][2] = Bishop(self.game, Color.BLACK)
        self.game.board[2][1] = Bishop(self.game, Color.BLACK)
        self.assertEqual(self.game.get_piece_coordinate(self.game.board[0][0]), Coordinate(0, 0))
        self.assertEqual(self.game.get_piece_coordinate(self.game.board[7][3]), Coordinate(7, 3))
        self.assertEqual(self.game.get_piece_coordinate(self.game.board[1][0]), Coordinate(1, 0))
        self.assertEqual(self.game.get_piece_coordinate(self.game.board[3][5]), Coordinate(3, 5))
        self.assertEqual(self.game.get_piece_coordinate(self.game.board[4][1]), Coordinate(4, 1))
        self.assertEqual(self.game.get_piece_coordinate(self.game.board[2][2]), Coordinate(2, 2))
        self.assertEqual(self.game.get_piece_coordinate(self.game.board[2][1]), Coordinate(2, 1))


class TestChessGame(unittest.TestCase):
    def test_to_piece_returns_correct_piece(self):
        game = ChessGame()
        p = game.to_piece("r")
        self.assertEqual(type(p), Rook)
        p = game.to_piece("R")
        self.assertEqual(type(p), Rook)

        p = game.to_piece("P")
        self.assertEqual(type(p), Pawn)
        p = game.to_piece("p")
        self.assertEqual(type(p), Pawn)

        p = game.to_piece("N")
        self.assertEqual(type(p), Knight)
        p = game.to_piece("n")
        self.assertEqual(type(p), Knight)

        p = game.to_piece("B")
        self.assertEqual(type(p), Bishop)
        p = game.to_piece("b")
        self.assertEqual(type(p), Bishop)

        p = game.to_piece("Q")
        self.assertEqual(type(p), Queen)
        p = game.to_piece("q")
        self.assertEqual(type(p), Queen)

        p = game.to_piece("K")
        self.assertEqual(type(p), King)
        p = game.to_piece("k")
        self.assertEqual(type(p), King)

    def test_load_fen_gives_correct_board(self):
        game = ChessGame()
        game.load_fen("8/8/8/8/8/8/8/8 w KQkq - 0 1")
        for row in range(8):
            for col in range(8):
                self.assertEqual(type(game.board[row][col]), Empty)

        game.load_fen("8/8/1r1R4/8/8/8/8/8 w KQkq - 0 1")
        self.assertEqual(type(game.board[5][1]), Rook)
        self.assertEqual(game.board[5][1].get_color(), Color.BLACK)

        self.assertEqual(type(game.board[5][3]), Rook)
        self.assertEqual(game.board[5][3].get_color(), Color.WHITE)

        game.load_fen("8/8/8/8/8/8/8/k7 w KQkq - 0 1")
        self.assertEqual(type(game.board[0][0]), King)
        self.assertEqual(game.board[0][0].get_color(), Color.BLACK)

    def test_load_fen_restores_correct_moves_and_clock(self):
        game = ChessGame()
        game.load_fen("8/8/8/8/8/8/8/8 w KQkq - 0 1")
        self.assertEqual(game.half_move_clock, 0)
        self.assertEqual(game.full_move_clock, 1)
        self.assertEqual(game.count, 0)

        game.load_fen("8/8/8/8/8/8/8/8 b KQkq - 10 15")
        self.assertEqual(game.half_move_clock, 10)
        self.assertEqual(game.full_move_clock, 15)
        self.assertEqual(game.count, 29)

        game.load_fen("8/8/8/8/8/8/8/8 w KQkq - 20 14")
        self.assertEqual(game.half_move_clock, 20)
        self.assertEqual(game.full_move_clock, 14)
        self.assertEqual(game.count, 26)

    def test_init_history_restores_expected_history(self):
        game = ChessGame()
        game.init_history([{"session_id": 15067, "src": '(1,3)', "tar": '(3,3)', "castling": False, "en_passant": False,
                            "en_passant_target_notation": 'd3', "half_move": 0, "full_move": 1},
                           {"session_id": 15067, "src": '(4,4)', "tar": '(5,2)', "castling": False, "en_passant": False,
                            "en_passant_target_notation": '-', "half_move": 50, "full_move": 31}])
        self.assertEqual(len(game.history), 2)
        self.assertEqual(game.history[-1]["src"], Coordinate(4, 4))
        self.assertEqual(game.history[-1]["tar"], Coordinate(5, 2))

        game.init_history([{"session_id": 32489, "src": '(2,2)', "tar": '(3,3)', "castling": False, "en_passant": False,
                            "en_passant_target_notation": 'd3', "half_move": 0, "full_move": 1},
                           {"session_id": 32489, "src": '(3,7)', "tar": '(1,4)', "castling": False, "en_passant": False,
                            "en_passant_target_notation": '-', "half_move": 50, "full_move": 31}])
        self.assertEqual(game.history[-1]["src"], Coordinate(3, 7))
        self.assertEqual(game.history[-1]["tar"], Coordinate(1, 4))
