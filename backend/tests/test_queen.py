import unittest
from api.piece.queen import Queen
from api.chess_game import ChessGame
from api.piece.piece_interface import Color
from api.piece.king import King


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)     # empty board
        self.chess_game.board[0][0] = Queen(self.chess_game, Color.WHITE, 0, 0)
        self.chess_game.board[3][3] = Queen(self.chess_game, Color.BLACK, 3, 3)
        self.chess_game.board[1][3] = King(self.chess_game, Color.BLACK, 1, 3)

    def test_get_moves(self):
        actual = self.chess_game.board[3][3].get_moves()
        expected = [(4, 3),
                    (5, 3),
                    (6, 3),
                    (7, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (3, 4),
                    (3, 5),
                    (3, 6),
                    (3, 7),
                    (2, 4),
                    (1, 5),
                    (0, 6),
                    (2, 3),
                    (2, 2),
                    (1, 1),
                    (0, 0),
                    (3, 2),
                    (3, 1),
                    (3, 0),
                    (4, 2),
                    (5, 1),
                    (6, 0)]
        for item in actual:
            self.assertTrue(item in expected)

    def test_get_checked_moves(self):
        self.chess_game.board[6][6] = King(self.chess_game, Color.WHITE, 6, 6)
        self.chess_game.board[5][5] = Queen(self.chess_game, Color.WHITE, 5, 5)
        self.chess_game.kings_coordinate = [(6, 6), (1, 3)]
        actual = self.chess_game.board[5][5].get_checked_moves()
        expected = {'moves': [(4, 4), (3, 3)]}
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
        actual_w = self.chess_game.board[0][0].to_string()
        actual_b = self.chess_game.board[3][3].to_string()
        expected_w = "Q"
        expected_b = "q"
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)
