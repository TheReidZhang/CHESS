import unittest
from api.chess_game import ChessGame
from api.piece.piece_interface import Color
from api.advanced_ai import AdvancedAI


class TestSimpleAI(unittest.TestCase):
    def test_game_evaluation_returns_correct_value(self):
        ai = AdvancedAI(ChessGame())
        ai.game.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.assertEqual(ai.game_evaluation(Color.WHITE), ai.game_evaluation(Color.BLACK))
        self.assertEqual(ai.game_evaluation(Color.WHITE), 0)

    def test_get_next_move_returns_correct_value(self):
        ai = AdvancedAI(ChessGame())
        move = ai.get_next_move()
        self.assertEqual(move, (0, 1, 2, 2))
        ai = AdvancedAI(ChessGame())
        ai.game.update((0, 1), (2, 2), "Queen", is_ai=True)
        move = ai.get_next_move()
        self.assertEqual(move, (6, 0, 5, 0))
