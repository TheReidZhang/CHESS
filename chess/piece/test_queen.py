import unittest
from chess.piece.queen import Queen
from chess.chess_game import ChessGame
from chess.piece.piece_interface import Color
from chess.piece.coordinate import Coordinate
from chess.piece.king import King


class TestRook(unittest.TestCase):
    def setUp(self) -> None:
        self.chess_game = ChessGame(fen="test")     # empty board
        self.chess_game.board[0][0] = Queen(self.chess_game, Color.WHITE)
        self.chess_game.board[3][3] = Queen(self.chess_game, Color.BLACK)
        self.chess_game.board[1][3] = King(self.chess_game, Color.BLACK)

    def test_get_moves(self):
        actual = self.chess_game.board[3][3].get_moves()
        expected = [Coordinate(4, 3),
                    Coordinate(5, 3),
                    Coordinate(6, 3),
                    Coordinate(7, 3),
                    Coordinate(2, 3),
                    Coordinate(3, 4),
                    Coordinate(3, 5),
                    Coordinate(3, 6),
                    Coordinate(3, 7),
                    Coordinate(3, 2),
                    Coordinate(3, 1),
                    Coordinate(3, 0),
                    Coordinate(4, 4),
                    Coordinate(5, 5),
                    Coordinate(6, 6),
                    Coordinate(7, 7),
                    Coordinate(2, 4),
                    Coordinate(1, 5),
                    Coordinate(0, 6),
                    Coordinate(4, 2),
                    Coordinate(5, 1),
                    Coordinate(6, 0),
                    Coordinate(2, 2),
                    Coordinate(1, 1),
                    Coordinate(0, 0)]
        self.assertEqual(actual, expected)

    def test_get_checked_moves(self):
        self.chess_game.board[6][6] = King(self.chess_game, Color.WHITE)
        self.chess_game.board[5][5] = Queen(self.chess_game, Color.WHITE)
        actual = self.chess_game.board[5][5].get_checked_moves()
        expected = {'moves': [Coordinate(4, 4), Coordinate(3, 3)]}
        self.assertEqual(actual, expected)

    def test_get_color(self):
        actual_w = self.chess_game.board[0][0].get_color()
        actual_b = self.chess_game.board[3][3].get_color()
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
