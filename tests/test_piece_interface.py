from chess.piece.piece_interface import PieceInterface
from unittest import TestCase


class TestIsValidCoord(TestCase):
    def test_is_valid_coord_valid(self):
        self.assertTrue(PieceInterface.is_valid_coord(7, 7))

    def test_is_valid_coord_invalid(self):
        self.assertFalse(PieceInterface.is_valid_coord(9, 7))
