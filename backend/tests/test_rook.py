import unittest
from api.piece.rook import Rook
from api.chess_game import ChessGame
from api.piece.piece_interface import Color
from api.piece.king import King


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)     # empty board
        self.chess_game.board[0][0] = Rook(self.chess_game, Color.WHITE, 0, 0)
        self.chess_game.board[2][3] = Rook(self.chess_game, Color.WHITE, 2, 3)
        self.chess_game.board[0][3] = King(self.chess_game, Color.WHITE, 0, 3)
        self.chess_game.board[3][3] = Rook(self.chess_game, Color.BLACK, 3, 3)
        self.chess_game.kings_coordinate = [(0, 3), (None, None)]

    def test_get_moves(self):
        actual = self.chess_game.board[2][3].get_moves()
        expected = [(3, 3),
                    (2, 4),
                    (2, 5),
                    (2, 6),
                    (2, 7),
                    (1, 3),
                    (2, 2),
                    (2, 1),
                    (2, 0)]
        for item in actual:
            self.assertTrue(item in expected)

    def test_get_checked_moves(self):
        actual = self.chess_game.board[2][3].get_checked_moves()
        expected = {'moves': [(3, 3), (1, 3)]}
        for item in actual["moves"]:
            self.assertTrue(item in expected["moves"])

    def test_get_color(self):
        actual_w = self.chess_game.board[0][0].color
        actual_b = self.chess_game.board[3][3].color
        expected_w = Color.WHITE
        expected_b = Color.BLACK
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)

    def test_to_string(self):
        actual_w = self.chess_game.board[2][3].to_string()
        actual_b = self.chess_game.board[3][3].to_string()
        expected_w = "R"
        expected_b = "r"
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)
