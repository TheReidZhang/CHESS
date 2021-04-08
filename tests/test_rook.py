import unittest
from chess.piece.rook import Rook
from chess.chess_game import ChessGame
from chess.piece.piece_interface import Color
from chess.piece.coordinate import Coordinate
from chess.piece.king import King


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)     # empty board
        self.chess_game.board[0][0] = Rook(self.chess_game, Color.WHITE)
        self.chess_game.board[2][3] = Rook(self.chess_game, Color.WHITE)
        self.chess_game.board[0][3] = King(self.chess_game, Color.WHITE)
        self.chess_game.board[3][3] = Rook(self.chess_game, Color.BLACK)

    def test_get_moves(self):
        actual = self.chess_game.board[2][3].get_moves()
        expected = [Coordinate(3, 3),
                    Coordinate(2, 4),
                    Coordinate(2, 5),
                    Coordinate(2, 6),
                    Coordinate(2, 7),
                    Coordinate(1, 3),
                    Coordinate(2, 2),
                    Coordinate(2, 1),
                    Coordinate(2, 0)]
        self.assertEqual(actual, expected)

    def test_get_checked_moves(self):
        actual = self.chess_game.board[2][3].get_checked_moves()
        expected = {'moves': [Coordinate(3, 3), Coordinate(1, 3)]}
        self.assertEqual(actual, expected)

    def test_get_color(self):
        actual_w = self.chess_game.board[0][0].get_color()
        actual_b = self.chess_game.board[3][3].get_color()
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