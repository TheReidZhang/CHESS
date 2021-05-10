import unittest
from api.piece.bishop import Bishop
from api.chess_game import ChessGame
from api.piece.piece_interface import Color
from api.piece.king import King


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)     # empty board
        self.chess_game.board[0][0] = Bishop(self.chess_game, Color.WHITE, 0, 0)
        self.chess_game.board[4][4] = Bishop(self.chess_game, Color.BLACK, 4, 4)
        self.chess_game.board[3][3] = Bishop(self.chess_game, Color.BLACK, 3, 3)

    def test_get_moves(self):
        actual = self.chess_game.board[3][3].get_moves()
        expected = [(2, 4),
                    (1, 5),
                    (0, 6),
                    (2, 2),
                    (1, 1),
                    (0, 0),
                    (4, 2),
                    (5, 1),
                    (6, 0)]
        for item in actual:
            self.assertTrue(item in expected)

    def test_get_checked_moves(self):
        self.chess_game.board[7][1] = King(self.chess_game, Color.BLACK, 7, 1)
        self.chess_game.board[0][6] = King(self.chess_game, Color.WHITE, 0, 6)
        self.chess_game.kings_coordinate = [(0, 6), (7, 1)]
        self.chess_game.board[3][5] = Bishop(self.chess_game, Color.WHITE, 3, 5)
        actual = self.chess_game.board[0][0].get_checked_moves()
        expected = {'moves': [(3, 3)]}
        self.assertEqual(actual, expected)

    def test_get_color(self):
        actual_w = self.chess_game.board[0][0].color
        actual_b = self.chess_game.board[3][3].color
        expected_w = Color.WHITE
        expected_b = Color.BLACK
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)

    def test_to_string(self):
        actual_w = self.chess_game.board[0][0].to_string()
        actual_b = self.chess_game.board[3][3].to_string()
        expected_w = "B"
        expected_b = "b"
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)
