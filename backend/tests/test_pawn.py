from api.piece.pawn import Pawn
from api.piece.king import King
from api.chess_game import ChessGame
from api.piece.coordinate import Coordinate
from api.piece.piece_interface import Color
from unittest import TestCase


class TestPawn(TestCase):
    def setUp(self) -> None:
        fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"
        self.chess_game = ChessGame(fen=fen)
        self.chess_game.board[0][4] = King(self.chess_game, Color.WHITE)
        self.chess_game.board[1][4] = Pawn(self.chess_game, Color.WHITE)
        self.chess_game.board[4][5] = Pawn(self.chess_game, Color.WHITE)
        self.chess_game.board[7][4] = King(self.chess_game, Color.BLACK)
        self.chess_game.board[4][4] = Pawn(self.chess_game, Color.BLACK)

        fen = "4k3/8/8/4pP2/8/8/4P3/4K3 w - e6 2 10"
        self.chess_game.history.append(fen)

    def test_en_passant_available(self):
        # fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        fen = "4k3/8/8/4pP2/8/8/4P3/4K3 w - e6 2 10"
        self.chess_game.history.append(fen)
        self.assertTrue(self.chess_game.board[4][5].en_passant(4, 4, 5))

    def test_en_passant_not_available(self):
        fen = "4k3/8/8/4pP2/8/8/4P3/4K3 w - e6 2 10"
        self.chess_game.history.append(fen)
        self.assertFalse(self.chess_game.board[4][5].en_passant(6, 4, 5))
        fen = "4k3/8/8/4pP2/8/8/4P3/4K3 w - - 2 10"
        self.chess_game.history.append(fen)
        # self.chess_game.history.append({
        #     "src": Coordinate(1, 4),
        #     "tar": Coordinate(2, 4),
        #     "src_piece": Pawn(self.chess_game, Color.WHITE),
        #     "tar_piece": Empty(self.chess_game, Color.EMPTY),
        #     "castling": False,
        #     "en_passant": False,
        #     "en_passant_target_notation": "-",
        #     "halfmove": 0,
        #     "fullmove": 1
        # })
        # self.chess_game.history.append({
        #     "src": Coordinate(7, 4),
        #     "tar": Coordinate(7, 3),
        #     "src_piece": King(self.chess_game, Color.BLACK),
        #     "tar_piece": Empty(self.chess_game, Color.EMPTY),
        #     "castling": False,
        #     "en_passant": False,
        #     "en_passant_target_notation": "-",
        #     "halfmove": 1,
        #     "fullmove": 2
        # })
        self.assertFalse(self.chess_game.board[4][5].en_passant(4, 4, 5))

        self.chess_game.history = []
        self.assertFalse(self.chess_game.board[4][5].en_passant(4, 4, 5))

    def test_get_moves(self):
        actual = self.chess_game.board[1][4].get_moves()
        expected = [Coordinate(2, 4), Coordinate(3, 4)]
        self.assertEqual(actual, expected)

    def test_get_moves_no_place_to_move(self):
        self.chess_game.board[7][0] = Pawn(self.chess_game, Color.WHITE)
        self.assertEqual(self.chess_game.board[7][0].get_moves(), [])

    def test_get_checked_moves(self):
        actual = self.chess_game.board[4][5].get_checked_moves()
        expected = {'moves': [Coordinate(5, 5), Coordinate(5, 4)]}
        self.assertEqual(actual, expected)

    def test_get_color(self):
        self.assertEqual(self.chess_game.board[4][5].get_color(), Color.WHITE)
        self.assertEqual(self.chess_game.board[4][4].get_color(), Color.BLACK)

    def test_to_string(self):
        self.assertEqual(self.chess_game.board[4][5].to_string(), "P")
        self.assertEqual(self.chess_game.board[4][4].to_string(), "p")
