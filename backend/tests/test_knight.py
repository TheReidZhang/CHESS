import unittest
from api.piece.knight import Knight
from api.piece.king import King
from api.chess_game import ChessGame
from api.piece.piece_interface import Color
from api.piece.coordinate import Coordinate


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)     # empty board
        self.chess_game.board[0][0] = Knight(self.chess_game, Color.WHITE)
        self.chess_game.board[0][2] = Knight(self.chess_game, Color.WHITE)
        self.chess_game.board[1][0] = Knight(self.chess_game, Color.BLACK)
        self.chess_game.board[1][2] = Knight(self.chess_game, Color.BLACK)

    def test_get_moves(self):
        actual = self.chess_game.board[1][2].get_moves()
        expected = [Coordinate(3, 3),
                    Coordinate(2, 4),
                    Coordinate(0, 4),
                    Coordinate(0, 0),
                    Coordinate(2, 0),
                    Coordinate(3, 1)]
        self.assertEqual(actual, expected)

    def test_get_checked_moves(self):
        self.chess_game.board[2][2] = King(self.chess_game, Color.WHITE)
        actual = self.chess_game.board[0][2].get_checked_moves()
        expected = {'moves': [Coordinate(1, 0)]}
        self.assertEqual(actual,expected)

    def test_get_color(self):
        actual_w = self.chess_game.board[0][0].get_color()
        actual_b = self.chess_game.board[1][2].get_color()
        expected_w = Color.WHITE
        expected_b = Color.BLACK
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)

    def test_to_string(self):
        actual_w = self.chess_game.board[0][2].to_string()
        actual_b = self.chess_game.board[1][2].to_string()
        expected_w = "N"
        expected_b = "n"
        self.assertEqual(actual_w, expected_w)
        self.assertEqual(actual_b, expected_b)
