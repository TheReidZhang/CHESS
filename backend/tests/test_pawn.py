from api.piece.pawn import Pawn
from api.piece.king import King
from api.chess_game import ChessGame
from api.piece.piece_interface import Color
from unittest import TestCase


class TestPawn(TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)
        self.chess_game.board[0][4] = King(self.chess_game, Color.WHITE, 0, 4)
        self.chess_game.board[1][4] = Pawn(self.chess_game, Color.WHITE, 1, 4)
        self.chess_game.board[4][5] = Pawn(self.chess_game, Color.WHITE, 4, 5)
        self.chess_game.board[7][4] = King(self.chess_game, Color.BLACK, 7, 4)
        self.chess_game.board[4][4] = Pawn(self.chess_game, Color.BLACK, 4, 4)
        self.chess_game.kings_coordinate = [(0, 4), (7, 4)]
        fen = "4k3/8/8/4pP2/8/8/4P3/4K3 w - e6 2 10"
        hist = {"fen": fen, "movement": {}}
        self.chess_game.history.append(hist)

    def test_en_passant_available(self):
        # fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        hist = {"fen": "4k3/8/8/4pP2/8/8/4P3/4K3 w - e6 2 10", "movement": {}}
        self.chess_game.history.append(hist)
        self.assertTrue(self.chess_game.board[4][5].en_passant(4, 4, 5))

    def test_en_passant_not_available(self):
        fen = "4k3/8/8/4pP2/8/8/4P3/4K3 w - e6 2 10"
        hist = {"fen": fen, "movement": {}}
        self.chess_game.history.append(hist)
        self.assertFalse(self.chess_game.board[4][5].en_passant(6, 4, 5))
        fen = "4k3/8/8/4pP2/8/8/4P3/4K3 w - - 2 10"
        hist = {"fen": fen, "movement": {}}
        self.chess_game.history.append(hist)
        self.assertFalse(self.chess_game.board[4][5].en_passant(4, 4, 5))

        self.chess_game.history = []
        self.assertFalse(self.chess_game.board[4][5].en_passant(4, 4, 5))

    def test_get_moves(self):
        actual = self.chess_game.board[1][4].get_moves()
        expected = [(2, 4), (3, 4)]
        self.assertEqual(actual, expected)

    def test_get_moves_no_place_to_move(self):
        self.chess_game.board[7][0] = Pawn(self.chess_game, Color.WHITE, 7, 0)
        self.assertEqual(self.chess_game.board[7][0].get_moves(), [])

    def test_get_checked_moves(self):
        actual = self.chess_game.board[4][5].get_checked_moves()
        expected = {'moves': [(5, 5), (5, 4)]}
        for item in actual["moves"]:
            self.assertTrue(item in expected["moves"])

    def test_get_color(self):
        self.assertEqual(self.chess_game.board[4][5].color, Color.WHITE)
        self.assertEqual(self.chess_game.board[4][4].color, Color.BLACK)

    def test_to_string(self):
        self.assertEqual(self.chess_game.board[4][5].to_string(), "P")
        self.assertEqual(self.chess_game.board[4][4].to_string(), "p")
