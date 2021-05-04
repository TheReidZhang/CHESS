from api.piece.utility import Coordinate
import unittest


class TestCoordinate(unittest.TestCase):
    def setUp(self) -> None:
        self.coordinate = Coordinate(1, 2)

    def test_get_tuple(self):
        self.assertEqual(self.coordinate.get_tuple(), (1, 2))

    def test_encode(self):
        self.assertEqual(self.coordinate.encode(), "c2")

    def test_decode(self):
        self.assertEqual(Coordinate.decode("c2"), self.coordinate)

    def test_encode_list(self):
        input_list = [Coordinate(1, 3), Coordinate(3, 7), Coordinate(6, 6)]
        actual = Coordinate.encode_list(input_list)
        expected = ["d2", "h4", "g7"]
        self.assertEqual(actual, expected)

    def test_eq_method(self):
        self.assertTrue(self.coordinate == Coordinate(1, 2))

    def test_str_method(self):
        self.assertEqual(str(self.coordinate), "(1,2)")

    def test_repr_method(self):
        self.assertEqual(repr(self.coordinate), "(1,2)")
