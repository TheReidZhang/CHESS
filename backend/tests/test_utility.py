from api.piece.utility import Utility
import unittest


class TestCoordinate(unittest.TestCase):

    def test_encode(self):
        self.assertEqual(Utility.encode(1, 2), "c2")
        self.assertEqual(Utility.encode(2, 2), "c3")
        self.assertEqual(Utility.encode(5, 3), "d6")
        self.assertEqual(Utility.encode(0, 0), "a1")
        self.assertEqual(Utility.encode(7, 7), "h8")

    def test_decode(self):
        self.assertEqual(Utility.decode("c2"), (1, 2))
        self.assertEqual(Utility.decode("c3"), (2, 2))
        self.assertEqual(Utility.decode("d6"), (5, 3))
        self.assertEqual(Utility.decode("a1"), (0, 0))
        self.assertEqual(Utility.decode("h8"), (7, 7))

    def test_encode_list(self):
        input_list = [(1, 3), (3, 7), (6, 6)]
        actual = Utility.encode_list(input_list)
        expected = ["d2", "h4", "g7"]
        self.assertEqual(actual, expected)
