import unittest
from api.chess_game import ChessGame
from api.piece.pawn import Pawn
from api.piece.knight import Knight
from api.piece.bishop import Bishop
from api.piece.king import King
from api.piece.queen import Queen
from api.piece.rook import Rook
from api.piece.empty import Empty
from api.piece.piece_interface import Color
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
            self.game.board[1][col] = Pawn(self.game, Color.WHITE, 1, col)
            self.game.board[6][col] = Pawn(self.game, Color.BLACK, 6, col)
        for row, color in [(0, Color.WHITE), (7, Color.BLACK)]:
            self.game.board[row][0] = Rook(self.game, color, row, 0)
            self.game.board[row][7] = Rook(self.game, color, row, 7)
            self.game.board[row][1] = Knight(self.game, color, row, 1)
            self.game.board[row][6] = Knight(self.game, color, row, 6)
            self.game.board[row][2] = Bishop(self.game, color, row, 2)
            self.game.board[row][5] = Bishop(self.game, color, row, 5)
            self.game.board[row][3] = Queen(self.game, color, row, 3)
            self.game.board[row][4] = King(self.game, color, row, 4)


class TestInitHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_init_history_restores_expected_history(self):
        history = [["", 1, "a2", "a4", "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1"],
                   ["", 2, "a7", "a5", "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq a6 0 2"],
                   ["", 3, "a1", "a3", "rnbqkbnr/1ppppppp/8/p7/P7/R7/1PPPPPPP/1NBQKBNR b Kkq - 1 2"],
                   ["", 4, "a8", "a6", "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPPP/1NBQKBNR w Kk - 2 3"],
                   ["", 5, "h2", "h4", "1nbqkbnr/1ppppppp/r7/p7/P6P/R7/1PPPPPP1/1NBQKBNR b Kk h3 0 3"],
                   ["", 6, "h7", "h5", "1nbqkbnr/1pppppp1/r7/p6p/P6P/R7/1PPPPPP1/1NBQKBNR w Kk h6 0 4"],
                   ["", 7, "h1", "h3", "1nbqkbnr/1pppppp1/r7/p6p/P6P/R6R/1PPPPPP1/1NBQKBN1 b k - 1 4"]]

        self.game.init_history(history)
        expected = [{"fen": "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1",
                     "movement": {"src": "a2", "tar": "a4"}},
                    {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq a6 0 2",
                     "movement": {"src": "a7", "tar": "a5"}},
                    {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/R7/1PPPPPPP/1NBQKBNR b Kkq - 1 2",
                     "movement": {"src": "a1", "tar": "a3"}},
                    {"fen": "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPPP/1NBQKBNR w Kk - 2 3",
                     "movement": {"src": "a8", "tar": "a6"}},
                    {"fen": "1nbqkbnr/1ppppppp/r7/p7/P6P/R7/1PPPPPP1/1NBQKBNR b Kk h3 0 3",
                     "movement": {"src": "h2", "tar": "h4"}},
                    {"fen": "1nbqkbnr/1pppppp1/r7/p6p/P6P/R7/1PPPPPP1/1NBQKBNR w Kk h6 0 4",
                     "movement": {"src": "h7", "tar": "h5"}},
                    {"fen": "1nbqkbnr/1pppppp1/r7/p6p/P6P/R6R/1PPPPPP1/1NBQKBN1 b k - 1 4",
                     "movement": {"src": "h1", "tar": "h3"}}]
        self.assertEqual(self.game.history[0], expected[0])
        self.assertEqual(self.game.history[1], expected[1])
        self.assertEqual(self.game.history[2], expected[2])
        self.assertEqual(self.game.history[3], expected[3])
        self.assertEqual(self.game.history[4], expected[4])
        self.assertEqual(self.game.history[5], expected[5])
        self.assertEqual(self.game.history[6], expected[6])

        self.assertEqual(len(history), 7)
        self.assertEqual(len(self.game.history), 7)


class TestGetGameHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_get_game_history_empty(self):
        self.game.history = []
        expected = []
        ret = self.game.get_game_history()
        self.assertEqual(ret, expected)

    def test_get_game_history_restores_expected_history(self):
        self.game.history = [{"fen": "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1",
                              "movement": {"src": "a2", "tar": "a4"}},
                             {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq a6 0 2",
                              "movement": {"src": "a7", "tar": "a5"}},
                             {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/R7/1PPPPPPP/1NBQKBNR b Kkq - 1 2",
                              "movement": {"src": "a1", "tar": "a3"}},
                             {"fen": "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPPP/1NBQKBNR w Kk - 2 3",
                              "movement": {"src": "a8", "tar": "a6"}},
                             {"fen": "1nbqkbnr/1ppppppp/r7/p7/P6P/R7/1PPPPPP1/1NBQKBNR b Kk h3 0 3",
                              "movement": {"src": "h2", "tar": "h4"}},
                             {"fen": "1nbqkbnr/1pppppp1/r7/p6p/P6P/R7/1PPPPPP1/1NBQKBNR w Kk h6 0 4",
                              "movement": {"src": "h7", "tar": "h5"}},
                             {"fen": "1nbqkbnr/1pppppp1/r7/p6p/P6P/R6R/1PPPPPP1/1NBQKBN1 b k - 1 4",
                              "movement": {"src": "h1", "tar": "h3"}}]
        expected = [{"src": "a2", "tar": "a4"}, {"src": "a7", "tar": "a5"}, {"src": "a1", "tar": "a3"},
                    {"src": "a8", "tar": "a6"}, {"src": "h2", "tar": "h4"}, {"src": "h7", "tar": "h5"},
                    {"src": "h1", "tar": "h3"}]
        ret = self.game.get_game_history()
        self.assertEqual(ret, expected)


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
                self.game.board[row][col] = Empty(None, Color.EMPTY, row, col)

    def test_get_checked_moves_checkmate(self):
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][4] = King(self.game, Color.BLACK, 7, 4)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE, 4, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK, 3, 3)
        self.game.turn = Color.WHITE

        checked_moves = self.game.get_checked_moves((4, 1))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in ["b2"])

        checked_moves = self.game.get_checked_moves((0, 0))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in ["a2"])

        checked_moves = self.game.get_checked_moves((4, 5))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in [])

    def test_get_checked_moves_checkmate2(self):
        self.game.board[0][3] = King(self.game, Color.WHITE, 0, 3)
        self.game.board[7][4] = King(self.game, Color.BLACK, 7, 4)
        self.game.board[1][2] = Pawn(self.game, Color.BLACK, 1, 2)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[3][4] = Bishop(self.game, Color.BLACK, 3, 4)
        self.game.turn = Color.WHITE

        checked_moves = self.game.get_checked_moves((0, 3))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in ["c1", "d2", "e1", "e2"])

        checked_moves = self.game.get_checked_moves((4, 1))
        moves = checked_moves["moves"]
        for move in moves:
            self.assertTrue(move in [])


class TestUpdateEnPassant(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_update_implement_en_passant(self):
        self.game.half_move_clock = 0
        self.game.full_move_clock = 10
        self.game.count = 20
        self.game.empty_cell = Empty(None, Color.EMPTY, -1, -1)
        self.game.history = [{"fen": "3q4/8/8/8/Pp6/8/8/5K2 b - a3 0 10",
                             "movement": {"src": "a2", "tar": "a4"}}]
        self.game.castling_notation = "-"
        self.game.turn = Color.BLACK
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = self.game.empty_cell
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.board[0][5] = King(self.game, Color.WHITE, 0, 5)
        self.game.board[3][0] = Pawn(self.game, Color.WHITE, 3, 0)
        self.game.board[3][1] = Pawn(self.game, Color.BLACK, 3, 1)
        self.game.update_en_passant((3, 1), (2, 0))
        self.assertEqual(self.game.board[3][0], self.game.empty_cell)


class TestUpdateEnPassantNotation(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_update_en_passant_notation(self):
        self.game.update_en_passant_notation((1, 0), (3, 0))
        self.assertEqual(self.game.en_passant_target_notation, "a3")

        self.game.update_en_passant_notation((1, 1), (3, 1))
        self.assertEqual(self.game.en_passant_target_notation, "b3")

        self.game.update_en_passant_notation((1, 2), (3, 2))
        self.assertEqual(self.game.en_passant_target_notation, "c3")

        self.game.update_en_passant_notation((1, 3), (3, 3))
        self.assertEqual(self.game.en_passant_target_notation, "d3")

        self.game.update_en_passant_notation((1, 4), (3, 4))
        self.assertEqual(self.game.en_passant_target_notation, "e3")

        self.game.update_en_passant_notation((1, 5), (3, 5))
        self.assertEqual(self.game.en_passant_target_notation, "f3")

        self.game.update_en_passant_notation((1, 6), (3, 6))
        self.assertEqual(self.game.en_passant_target_notation, "g3")

        self.game.update_en_passant_notation((1, 7), (3, 7))
        self.assertEqual(self.game.en_passant_target_notation, "h3")

        self.game.update_en_passant_notation((6, 0), (4, 0))
        self.assertEqual(self.game.en_passant_target_notation, "a6")

        self.game.update_en_passant_notation((6, 1), (4, 1))
        self.assertEqual(self.game.en_passant_target_notation, "b6")

        self.game.update_en_passant_notation((6, 2), (4, 2))
        self.assertEqual(self.game.en_passant_target_notation, "c6")

        self.game.update_en_passant_notation((6, 3), (4, 3))
        self.assertEqual(self.game.en_passant_target_notation, "d6")

        self.game.update_en_passant_notation((6, 4), (4, 4))
        self.assertEqual(self.game.en_passant_target_notation, "e6")

        self.game.update_en_passant_notation((6, 5), (4, 5))
        self.assertEqual(self.game.en_passant_target_notation, "f6")

        self.game.update_en_passant_notation((6, 6), (4, 6))
        self.assertEqual(self.game.en_passant_target_notation, "g6")

        self.game.update_en_passant_notation((6, 7), (4, 7))
        self.assertEqual(self.game.en_passant_target_notation, "h6")


class TestUpdateCastle(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_update_castle(self):
        self.game.half_move_clock = 0
        self.game.full_move_clock = 10
        self.game.count = 20
        self.game.empty_cell = Empty(None, Color.EMPTY, -1, -1)
        self.game.history = [{"fen": "r3k3/8/8/8/Pp6/8/8/4K2R b Kq a3 0 10",
                              "movement": {"src": "a2", "tar": "a4"}}]
        self.game.turn = Color.BLACK
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = self.game.empty_cell
        self.game.board[7][4] = King(self.game, Color.BLACK, 7, 4)
        self.game.board[7][4].firstMove = True
        self.game.board[7][0] = Rook(self.game, Color.BLACK, 7, 0)
        self.game.board[7][0].firstMove = True
        self.game.board[0][4] = King(self.game, Color.WHITE, 0, 4)
        self.game.board[0][4].firstMove = True
        self.game.board[0][7] = Rook(self.game, Color.WHITE, 0, 7)
        self.game.board[0][7].firstMove = True
        self.game.board[3][0] = Pawn(self.game, Color.WHITE, 3, 0)
        self.game.board[3][1] = Pawn(self.game, Color.BLACK, 3, 1)
        expected_1 = self.game.board[7][0]
        expected_2 = self.game.board[0][7]

        self.game.update_castle((7, 4), (7, 2))
        self.assertEqual(self.game.board[7][3], expected_1)

        self.game.update_castle((0, 4), (0, 6))
        self.assertEqual(self.game.board[0][5], expected_2)


class TestUpdateMovementClock(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_update_movement_clock(self):
        self.game.update_movement_clock((1, 0), (3, 0))
        self.assertEqual(self.game.count, 1)
        self.assertEqual(self.game.full_move_clock, 1)
        self.assertEqual(self.game.half_move_clock, 0)

        self.game.update_movement_clock((6, 0), (4, 0))
        self.assertEqual(self.game.count, 2)
        self.assertEqual(self.game.full_move_clock, 2)
        self.assertEqual(self.game.half_move_clock, 0)

        self.game.update_movement_clock((0, 6), (2, 5))
        self.assertEqual(self.game.count, 3)
        self.assertEqual(self.game.full_move_clock, 2)
        self.assertEqual(self.game.half_move_clock, 1)

        self.game.update_movement_clock((6, 3), (5, 3))
        self.assertEqual(self.game.count, 4)
        self.assertEqual(self.game.full_move_clock, 3)
        self.assertEqual(self.game.half_move_clock, 0)

        self.game.update_movement_clock((0, 1), (2, 2))
        self.assertEqual(self.game.count, 5)
        self.assertEqual(self.game.full_move_clock, 3)
        self.assertEqual(self.game.half_move_clock, 1)

        self.game.update_movement_clock((7, 0), (5, 0))
        self.game.update_movement_clock((1, 4), (3, 4))
        self.game.update_movement_clock((7, 1), (5, 2))
        self.assertEqual(self.game.count, 8)
        self.assertEqual(self.game.full_move_clock, 5)
        self.assertEqual(self.game.half_move_clock, 1)

        self.game.board[5][0] = Rook(self, Color.BLACK, 5, 0)
        self.game.update_movement_clock((0, 5), (5, 0))
        self.assertEqual(self.game.count, 9)
        self.assertEqual(self.game.full_move_clock, 5)
        self.assertEqual(self.game.half_move_clock, 0)


class TestUpdatePromotion(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_update_implement_promotion(self):
        self.game.half_move_clock = 0
        self.game.full_move_clock = 10
        self.game.count = 20
        self.game.empty_cell = Empty(None, Color.EMPTY, -1, -1)
        self.game.history = [{"fen": "3bk3/PP6/8/8/8/8/6pp/4KB2 w - - 0 10",
                              "movement": {"src": "a6", "tar": "a7"}}]
        self.game.turn = Color.WHITE
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = self.game.empty_cell
        self.game.board[7][4] = King(self.game, Color.BLACK, 7, 4)
        self.game.board[7][3] = Bishop(self.game, Color.BLACK, 7, 3)
        self.game.board[7][4].firstMove = True
        self.game.board[0][4] = King(self.game, Color.WHITE, 0, 4)
        self.game.board[0][5] = Rook(self.game, Color.WHITE, 0, 5)
        self.game.board[0][4].firstMove = True
        self.game.board[6][0] = Pawn(self.game, Color.WHITE, 6, 0)
        self.game.board[1][7] = Pawn(self.game, Color.BLACK, 1, 7)
        self.game.board[6][1] = Pawn(self.game, Color.WHITE, 6, 1)
        self.game.board[1][6] = Pawn(self.game, Color.BLACK, 1, 6)

        self.game.update_promotion((6, 0), (7, 0), "Queen")
        self.assertEqual(type(self.game.board[7][0]), Queen)
        self.assertEqual(self.game.board[7][0].color, Color.WHITE)

        self.game.update_promotion((1, 7), (0, 7), "Rook")
        self.assertEqual(type(self.game.board[0][7]), Rook)
        self.assertEqual(self.game.board[0][7].color, Color.BLACK)

        self.game.update_promotion((6, 1), (7, 1), "Bishop")
        self.assertEqual(type(self.game.board[7][1]), Bishop)
        self.assertEqual(self.game.board[7][0].color, Color.WHITE)

        self.game.update_promotion((1, 6), (0, 6), "Knight")
        self.assertEqual(type(self.game.board[0][6]), Knight)
        self.assertEqual(self.game.board[0][6].color, Color.BLACK)


class TestUpDate(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_update_start_move_black(self):
        random_num_1 = random.randint(0, 7)
        random_num_2 = random.randint(0, 7)
        for row in range(6, 8):
            for col in range(8):
                self.assertFalse(self.game.update((row, col),
                                 (random_num_1, random_num_2), "Queen"))

    def test_update_ended_without_continue(self):
        self.game.half_move_clock = 49
        self.game.full_move_clock = 100
        self.game.count = 200
        self.game.en_passant_target_notation = "-"
        self.game.castling_notation = "-"
        self.game.turn = Color.WHITE
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.board[0][5] = King(self.game, Color.WHITE, 0, 5)
        self.assertTrue(self.game.update((0, 5), (0, 4), "Queen"))
        self.assertFalse(self.game.update((7, 3), (7, 2), "Queen"))

    def test_update_move_pawn(self):
        for col in range(8):
            self.assertTrue(self.game.update((1, col), (3, col), "Queen"))
            self.assertEqual(self.game.en_passant_target_notation, chr(ord('a') + col) + "3")
            self.game.turn = Color.WHITE
        for col in range(8):
            self.assertTrue(self.game.update((3, col), (4, col), "Queen"))
            self.game.turn = Color.WHITE

    def test_update_move_white(self):
        random_num_1 = random.randint(0, 7)
        random_num_2 = random.randint(0, 7)
        self.assertFalse(self.game.update((0, 0), (random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.update((0, 1), (2, 0), "Queen"))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.update((2, 0), (0, 1), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update((0, 2), (random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update((0, 3), (random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update((0, 4), (random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update((0, 5), (random_num_1, random_num_2), "Queen"))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.update((0, 6), (2, 7), "Queen"))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.update((2, 7), (0, 6), "Queen"))
        self.game.turn = Color.WHITE
        self.assertFalse(self.game.update((0, 7), (random_num_1, random_num_2), "Queen"))

    def test_update_kings_coordinate(self):
        self.game.update((1, 4), (3, 4), "Queen")
        self.game.update((6, 4), (4, 4), "Queen")
        self.game.update((0, 4), (1, 4), "Queen")
        self.game.update((7, 4), (6, 4), "Queen")
        self.assertEqual(self.game.kings_coordinate[0], (1, 4))
        self.assertEqual(self.game.kings_coordinate[1], (6, 4))

    def test_update_history(self):
        self.game.update((1, 0), (3, 0), "Queen")
        self.game.update((6, 0), (4, 0), "Queen")
        self.game.update((0, 0), (2, 0), "Queen")
        self.game.update((7, 0), (5, 0), "Queen")
        self.game.update((1, 7), (3, 7), "Queen")
        self.game.update((6, 7), (4, 7), "Queen")
        self.game.update((0, 7), (2, 7), "Queen")
        self.game.update((7, 7), (5, 7), "Queen")

        self.assertEqual(self.game.history[0]["fen"], "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1")
        self.assertEqual(self.game.history[0]["movement"], {"src": "a2", "tar": "a4"})

        self.assertEqual(self.game.history[1]["fen"], "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq a6 0 2")
        self.assertEqual(self.game.history[1]["movement"], {"src": "a7", "tar": "a5"})

        self.assertEqual(self.game.history[2]["fen"], "rnbqkbnr/1ppppppp/8/p7/P7/R7/1PPPPPPP/1NBQKBNR b Kkq - 1 2")
        self.assertEqual(self.game.history[2]["movement"], {"src": "a1", "tar": "a3"})

        self.assertEqual(self.game.history[3]["fen"], "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPPP/1NBQKBNR w Kk - 2 3")
        self.assertEqual(self.game.history[3]["movement"], {"src": "a8", "tar": "a6"})

        self.assertEqual(self.game.history[4]["fen"], "1nbqkbnr/1ppppppp/r7/p7/P6P/R7/1PPPPPP1/1NBQKBNR b Kk h3 0 3")
        self.assertEqual(self.game.history[4]["movement"], {"src": "h2", "tar": "h4"})

        self.assertEqual(self.game.history[5]["fen"], "1nbqkbnr/1pppppp1/r7/p6p/P6P/R7/1PPPPPP1/1NBQKBNR w Kk h6 0 4")
        self.assertEqual(self.game.history[5]["movement"], {"src": "h7", "tar": "h5"})

        self.assertEqual(self.game.history[6]["fen"], "1nbqkbnr/1pppppp1/r7/p6p/P6P/R6R/1PPPPPP1/1NBQKBN1 b k - 1 4")
        self.assertEqual(self.game.history[6]["movement"], {"src": "h1", "tar": "h3"})

        self.assertEqual(self.game.history[7]["fen"], "1nbqkbn1/1pppppp1/r6r/p6p/P6P/R6R/1PPPPPP1/1NBQKBN1 w - - 2 5")
        self.assertEqual(self.game.history[7]["movement"], {"src": "h8", "tar": "h6"})


class TestUndo(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_undo_init(self):
        self.game.undo()
        self.assertEqual(self.game.turn, Color.WHITE)
        self.assertEqual(self.game.history, [])

    def test_undo_first_step(self):
        self.game.history = [{"fen": "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1",
                              "movement": {"src": "a2", "tar": "a4"}}]
        self.game.turn = Color.BLACK
        self.game.undo()
        self.assertEqual(self.game.turn, Color.WHITE)
        self.assertEqual(self.game.history, [])

    def test_undo(self):
        self.game.history = [{"fen": "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1",
                             "movement": {"src": "a2", "tar": "a4"}},
                             {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq a6 0 2",
                              "movement": {"src": "a7", "tar": "a5"}},
                             {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/R7/1PPPPPPP/1NBQKBNR b Kkq - 1 2",
                              "movement": {"src": "a1", "tar": "a3"}},
                             {"fen": "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPP1/1NBQKBNR w Kk - 2 3",
                              "movement": {"src": "a8", "tar": "a6"}}]
        self.game.undo()
        color = Color.BLACK
        self.assertEqual(self.game.turn, color)
        self.assertEqual(self.game.castling_notation, "Kkq")
        self.assertEqual(self.game.en_passant_target_notation, "-")
        self.assertEqual(self.game.half_move_clock, 1)
        self.assertEqual(self.game.full_move_clock, 2)
        self.assertEqual(self.game.board[0][0], self.game.empty_cell)
        self.assertEqual(type(self.game.board[0][1]), Knight)
        self.assertEqual(self.game.board[0][1].color, Color.WHITE)
        self.assertEqual(type(self.game.board[0][2]), Bishop)
        self.assertEqual(type(self.game.board[0][3]), Queen)
        self.assertEqual(type(self.game.board[0][4]), King)
        self.assertEqual(type(self.game.board[0][5]), Bishop)
        self.assertEqual(type(self.game.board[0][6]), Knight)
        self.assertEqual(type(self.game.board[0][7]), Rook)
        self.assertEqual(type(self.game.board[7][0]), Rook)
        self.assertEqual(type(self.game.board[7][1]), Knight)
        self.assertEqual(self.game.board[7][1].color, Color.BLACK)
        self.assertEqual(type(self.game.board[7][2]), Bishop)
        self.assertEqual(type(self.game.board[7][3]), Queen)
        self.assertEqual(type(self.game.board[7][4]), King)
        self.assertEqual(type(self.game.board[7][5]), Bishop)
        self.assertEqual(type(self.game.board[7][6]), Knight)
        self.assertEqual(type(self.game.board[7][7]), Rook)


class TestGetHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_get_history_start(self):
        self.assertEqual(self.game.get_history(), {})

    def test_get_history_during_game(self):
        self.game.history = [{"fen": "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1",
                             "movement": {"src": "a2", "tar": "a4"}},
                             {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq a6 0 2",
                              "movement": {"src": "a7", "tar": "a5"}},
                             {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/R7/1PPPPPPP/1NBQKBNR b Kkq - 1 2",
                              "movement": {"src": "a1", "tar": "a3"}},
                             {"fen": "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPP1/1NBQKBNR w Kk - 2 3",
                              "movement": {"src": "a8", "tar": "a6"}}]
        expect = {"src": "a8", "tar": "a6", "fen": "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPP1/1NBQKBNR w Kk - 2 3",
                  "step": 4}
        self.assertEqual(self.game.get_history(), expect)


class TestKingCoordinate(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_king_coordinate_start(self):
        self.assertEqual(self.game.king_coordinate(Color.WHITE), (0, 4))
        self.assertEqual(self.game.king_coordinate(Color.BLACK), (7, 4))

    def test_king_coordinate(self):
        self.game.kings_coordinate = [(0, 0), (7, 3)]
        self.assertEqual(self.game.king_coordinate(Color.WHITE), (0, 0))
        self.assertEqual(self.game.king_coordinate(Color.BLACK), (7, 3))


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
        self.game.board[0][4].firstMove = True
        self.game.board[7][4].firstMove = True
        self.game.board[0][0].firstMove = True
        self.game.board[0][7].firstMove = True
        self.game.board[7][0].firstMove = True
        self.game.board[7][7].firstMove = True
        self.assertEqual(self.game.get_castling_notation(), "KQkq")

        self.game.board[0][0].firstMove = False
        self.assertEqual(self.game.get_castling_notation(), "Kkq")

        self.game.board[0][7].firstMove = False
        self.assertEqual(self.game.get_castling_notation(), "kq")

        self.game.board[7][0].firstMove = False
        self.assertEqual(self.game.get_castling_notation(), "k")

        self.game.board[7][7].firstMove = False
        self.assertEqual(self.game.get_castling_notation(), "-")


class TestGetFen(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_get_fen_start(self):
        self.assertEqual(self.game.get_fen(),
                         "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_get_fen_during_game(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE, 4, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK, 3, 3)
        self.game.history = [{"src": (0, 4)}, {"src": (7, 4)}]
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
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 0), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE, 4, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK, 3, 3)
        self.assertTrue(self.game.is_being_checked())

    def test_is_being_checked_during_game_false(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][4] = King(self.game, Color.WHITE, 0, 4)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 4), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE, 4, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK, 3, 3)
        self.assertFalse(self.game.is_being_checked())


class TestIsBeingCheckedAfterMove(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_is_being_checked_after_move_start(self):
        self.assertFalse(self.game.is_being_checked_after_move((1, 4), (3, 4)))

    def test_is_being_checked_after_move_in_few_moves(self):
        self.assertFalse(self.game.is_being_checked_after_move((6, 2), (4, 2)))
        self.assertFalse(self.game.is_being_checked_after_move((0, 6), (2, 5)))
        self.assertFalse(self.game.is_being_checked_after_move((0, 6), (2, 5)))
        self.assertFalse(self.game.is_being_checked_after_move((6, 0), (4, 0)))
        self.assertFalse(self.game.is_being_checked_after_move((0, 7), (0, 6)))
        self.assertFalse(self.game.is_being_checked_after_move((7, 0), (6, 0)))
        self.assertFalse(self.game.is_being_checked_after_move((1, 0), (3, 0)))
        self.assertFalse(self.game.is_being_checked_after_move((6, 7), (4, 7)))
        self.assertFalse(self.game.is_being_checked_after_move((0, 0), (1, 0)))
        self.assertFalse(self.game.is_being_checked_after_move((7, 7), (6, 7)))

    def test_is_being_checked_after_move_during_game_true(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 0), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE, 4, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[4][2] = Bishop(self.game, Color.BLACK, 4, 2)
        self.assertTrue(self.game.is_being_checked_after_move((4, 2), (3, 3)))

    def test_is_being_checked_after_move_during_game_false(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][4] = King(self.game, Color.WHITE, 0, 4)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 4), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE, 4, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[4][2] = Bishop(self.game, Color.BLACK, 4, 2)
        self.assertFalse(self.game.is_being_checked_after_move((4, 2), (2, 4)))


class TestCheckGameStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_check_game_status_start(self):
        self.assertEqual(self.game.check_game_status(), "Continue")

    def test_check_game_status_half_move_draw(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 0), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[3][5] = Pawn(self.game, Color.WHITE, 3, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[2][0] = Bishop(self.game, Color.BLACK, 2, 0)
        self.game.board[2][1] = Bishop(self.game, Color.BLACK, 2, 1)
        self.game.half_move_clock = 50
        self.assertEqual(self.game.check_game_status(), "Draw")

    def test_check_game_status_without_check_draw(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 0), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[2][0] = Bishop(self.game, Color.BLACK, 2, 0)
        self.game.board[2][1] = Bishop(self.game, Color.BLACK, 2, 1)
        self.assertEqual(self.game.check_game_status(), "Draw")

    def test_check_game_status_without_check_continue(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 0), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[2][5] = Pawn(self.game, Color.WHITE, 2, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[2][0] = Bishop(self.game, Color.BLACK, 2, 0)
        self.assertEqual(self.game.check_game_status(), "Continue")

    def test_check_game_status_with_check_continue(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 0), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[4][5] = Pawn(self.game, Color.WHITE, 4, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[3][3] = Bishop(self.game, Color.BLACK, 3, 3)
        self.assertEqual(self.game.check_game_status(), "Continue")

    def test_check_game_status_with_check_loss(self):
        empty = Empty(None, Color.EMPTY, -1, -1)
        for row in range(8):
            for col in range(8):
                self.game.board[row][col] = empty
        self.game.board[0][0] = King(self.game, Color.WHITE, 0, 0)
        self.game.board[7][3] = King(self.game, Color.BLACK, 7, 3)
        self.game.kings_coordinate = [(0, 0), (7, 3)]
        self.game.board[1][0] = Pawn(self.game, Color.BLACK, 1, 0)
        self.game.board[3][5] = Pawn(self.game, Color.WHITE, 3, 5)
        self.game.board[4][1] = Rook(self.game, Color.WHITE, 4, 1)
        self.game.board[2][2] = Bishop(self.game, Color.BLACK, 2, 2)
        self.game.board[2][1] = Bishop(self.game, Color.BLACK, 2, 1)
        self.assertEqual(self.game.check_game_status(), "WhiteLoss")


class TestToPiece(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_to_piece_returns_correct_piece(self):
        piece = self.game.to_piece("r", 7, 0)
        self.assertEqual(type(piece), Rook)
        self.assertEqual(piece.color, Color.BLACK)

        piece = self.game.to_piece("R", 0, 0)
        self.assertEqual(type(piece), Rook)
        self.assertEqual(piece.color, Color.WHITE)

        piece = self.game.to_piece("P", 1, 0)
        self.assertEqual(type(piece), Pawn)
        self.assertEqual(piece.color, Color.WHITE)

        piece = self.game.to_piece("p", 6, 0)
        self.assertEqual(type(piece), Pawn)
        self.assertEqual(piece.color, Color.BLACK)

        piece = self.game.to_piece("N", 0, 1)
        self.assertEqual(type(piece), Knight)
        self.assertEqual(piece.color, Color.WHITE)

        piece = self.game.to_piece("n", 7, 1)
        self.assertEqual(type(piece), Knight)
        self.assertEqual(piece.color, Color.BLACK)

        piece = self.game.to_piece("B", 0, 2)
        self.assertEqual(type(piece), Bishop)
        self.assertEqual(piece.color, Color.WHITE)

        piece = self.game.to_piece("b", 7, 2)
        self.assertEqual(type(piece), Bishop)
        self.assertEqual(piece.color, Color.BLACK)

        piece = self.game.to_piece("Q", 0, 3)
        self.assertEqual(type(piece), Queen)
        self.assertEqual(piece.color, Color.WHITE)

        piece = self.game.to_piece("q", 7, 3)
        self.assertEqual(type(piece), Queen)
        self.assertEqual(piece.color, Color.BLACK)

        piece = self.game.to_piece("K", 0, 4)
        self.assertEqual(type(piece), King)
        self.assertEqual(piece.color, Color.WHITE)

        piece = self.game.to_piece("k", 7, 4)
        self.assertEqual(type(piece), King)
        self.assertEqual(piece.color, Color.BLACK)


class TestLoadFen(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_load_fen_gives_correct_board(self):
        game = ChessGame()
        game.load_fen("8/8/8/8/8/8/8/8 w KQkq - 0 1")
        for row in range(8):
            for col in range(8):
                self.assertEqual(type(game.board[row][col]), Empty)

        game.load_fen("8/8/1r1R4/8/8/8/8/8 w KQkq - 0 1")
        self.assertEqual(type(game.board[5][1]), Rook)
        self.assertEqual(game.board[5][1].color, Color.BLACK)

        self.assertEqual(type(game.board[5][3]), Rook)
        self.assertEqual(game.board[5][3].color, Color.WHITE)

        game.load_fen("8/8/8/8/8/8/8/k7 w KQkq - 0 1")
        self.assertEqual(type(game.board[0][0]), King)
        self.assertEqual(game.board[0][0].color, Color.BLACK)

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

        game.load_fen("8/8/8/8/8/8/8/8 w - - 20 14")
        self.assertEqual(game.half_move_clock, 20)
        self.assertEqual(game.full_move_clock, 14)
        self.assertEqual(game.count, 26)
