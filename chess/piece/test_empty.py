import unittest
from chess.piece.empty import Empty
from chess.chess_game import ChessGame
from chess.piece.piece_interface import Color


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        self.chess_game = ChessGame(fen="test")     # empty board
        self.chess_game.board[3][3] = Empty(self.chess_game, Color.EMPTY)

    def test_get_moves(self):
        actual = self.chess_game.board[3][3].get_moves()
        expected = []
        self.assertEqual(actual, expected)

    def test_get_checked_moves(self):
        actual = self.chess_game.board[3][3].get_checked_moves()
        expected = {'moves': []}
        self.assertEqual(actual, expected)

    def test_get_color(self):
        actual = self.chess_game.board[3][3].get_color()
        expected = Color.EMPTY
        self.assertEqual(actual, expected)

    def test_to_string(self):
        actual = self.chess_game.board[3][3].to_string()
        expected = "*"
        self.assertEqual(actual, expected)
