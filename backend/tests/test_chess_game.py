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
from api.piece.coordinate import Coordinate
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


class TestInitHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

    def test_init_history_restores_expected_history(self):
        history = [{"fen": "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1",
                    "movement": {"src": "a7", "tar": "a5"}},
                   {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq a6 0 2",
                    "movement": {"src": "a7", "tar": "a5"}},
                   {"fen": "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPPP/1NBQKBNR w Kk a6 2 3",
                    "movement": {"src": "a7", "tar": "a5"}},
                   {"fen": "1nbqkbnr/1ppppppp/r7/p7/P6P/R7/1PPPPPP1/1NBQKBNR b Kk h3 0 3",
                    "movement": {"src": "h2", "tar": "h4"}}]
        self.game.init_history(history)
        self.assertEqual(self.game.history[0], {"fen": "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq a3 0 1",
                                                "movement": {"src": "a7", "tar": "a5"}})
        self.assertEqual(self.game.history[1], {"fen": "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq a6 0 2",
                                                "movement": {"src": "a7", "tar": "a5"}})
        self.assertEqual(self.game.history[2], {"fen": "1nbqkbnr/1ppppppp/r7/p7/P7/R7/1PPPPPPP/1NBQKBNR w Kk a6 2 3",
                                                "movement": {"src": "a7", "tar": "a5"}})
        self.assertEqual(self.game.history[3], {"fen": "1nbqkbnr/1ppppppp/r7/p7/P6P/R7/1PPPPPP1/1NBQKBNR b Kk h3 0 3",
                                                "movement": {"src": "h2", "tar": "h4"}})

        history.append({"fen": "1nbqkbnr/1pppppp1/r7/p6p/P6P/R7/1PPPPPP1/1NBQKBNR w Kk h6 0 4",
                        "movement": {"src": "h7", "tar": "h5"}})
        self.assertEqual(len(history), 5)
        self.assertEqual(len(self.game.history), 5)


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
        self.game.update(Coordinate(6, 0), Coordinate(4, 0), "Queen")
        self.game.update(Coordinate(0, 0), Coordinate(2, 0), "Queen")
        self.game.update(Coordinate(7, 0), Coordinate(5, 0), "Queen")
        self.game.update(Coordinate(1, 7), Coordinate(3, 7), "Queen")
        self.game.update(Coordinate(6, 7), Coordinate(4, 7), "Queen")

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


class TestUndo(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame(fen="start")

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
        piece = game.to_piece("r")
        self.assertEqual(type(piece), Rook)
        piece = game.to_piece("R")
        self.assertEqual(type(piece), Rook)

        piece = game.to_piece("P")
        self.assertEqual(type(piece), Pawn)
        piece = game.to_piece("p")
        self.assertEqual(type(piece), Pawn)

        piece = game.to_piece("N")
        self.assertEqual(type(piece), Knight)
        piece = game.to_piece("n")
        self.assertEqual(type(piece), Knight)

        piece = game.to_piece("B")
        self.assertEqual(type(piece), Bishop)
        piece = game.to_piece("b")
        self.assertEqual(type(piece), Bishop)

        piece = game.to_piece("Q")
        self.assertEqual(type(piece), Queen)
        piece = game.to_piece("q")
        self.assertEqual(type(piece), Queen)

        piece = game.to_piece("K")
        self.assertEqual(type(piece), King)
        piece = game.to_piece("k")
        self.assertEqual(type(piece), King)

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
