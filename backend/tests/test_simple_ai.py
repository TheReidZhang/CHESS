import unittest
from api.chess_game import ChessGame
from api.piece.rook import Rook
from api.piece.piece_interface import Color
from api.piece.utility import Coordinate
from api.simple_ai import SimpleAI


class TestSimpleAI(unittest.TestCase):
    def test_get_value_returns_correct_value(self):
        simple_ai = SimpleAI(ChessGame())
        self.assertEqual(simple_ai.get_value(simple_ai.game.board), -39)

        simple_ai.game.board[6][0] = simple_ai.game.empty_cell
        self.assertEqual(simple_ai.get_value(simple_ai.game.board), -38)

        simple_ai.game.board[6][0] = Rook(simple_ai.game, Color.BLACK)
        self.assertEqual(simple_ai.get_value(simple_ai.game.board), -43)

    def test_get_next_move_returns_correct_value(self):
        simple_ai = SimpleAI(ChessGame())
        move = simple_ai.get_next_move()
        self.assertEqual(move, (0, 1, 2, 2))

        simple_ai = SimpleAI(ChessGame())
        simple_ai.game.update(Coordinate(0, 1), Coordinate(2, 2), "Queen")
        move = simple_ai.get_next_move()
        self.assertEqual(move, (6, 2, 5, 2))
