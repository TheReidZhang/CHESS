import unittest
from api.piece.empty import Empty
from api.chess_game import ChessGame
from api.piece.piece_interface import Color


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)     # empty board
        self.chess_game.board[3][3] = Empty(self.chess_game, Color.EMPTY, 3, 3)

    def test_get_moves(self):
        actual = self.chess_game.board[3][3].get_moves()
        expected = []
        self.assertEqual(actual, expected)

    def test_get_checked_moves(self):
        actual = self.chess_game.board[3][3].get_checked_moves()
        expected = {'moves': []}
        self.assertEqual(actual, expected)

    def test_get_color(self):
        actual = self.chess_game.board[3][3].color
        expected = Color.EMPTY
        self.assertEqual(actual, expected)

    def test_to_string(self):
        actual = self.chess_game.board[3][3].to_string()
        expected = "*"
        self.assertEqual(actual, expected)
