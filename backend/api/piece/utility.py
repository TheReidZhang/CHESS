class Utility:
    @staticmethod
    def encode(x: int, y: int) -> str:
        """
        The columns are 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'
        The rows are '1', '2', '3', '4', '5', '6', '7', '8'
        An example: Coordinate(0,0) is the bottom left corner of the board. After encoding, it becomes 'a1'.
        :return: coordinate of a square in string type
        """
        return chr(ord('a') + y) + str(x + 1)

    @staticmethod
    def decode(pos: str) -> tuple:
        """
        Decode str coordinates into tuple of integer coordinates
        Decode 'a1' -> (0,0)
        :param pos: a str representing a coordinate of board
        :return: an object of Coordinate representing the str coordinates
        """
        return int(pos[1]) - 1, ord(pos[0]) - ord('a')

    @staticmethod
    def encode_list(lst: [tuple]) -> [str]:
        """
        Encode a list of objects of Coordinates into a list of str coordinates
        Encode [Coordinate(0,0), Coordinate(7,7)] -> ['a1', 'h8']
        :param lst: a list of objects of Coordinates
        :return: a list of str coordinates
        """
        ret = []
        for coord in lst:
            ret.append(Utility.encode(coord[0], coord[1]))
        return ret
