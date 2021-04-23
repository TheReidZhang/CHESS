class Coordinate:
    """
    Represents the location of pieces on board
    """
    def __init__(self, x: int, y: int):
        """
        x:0,y:0 is the bottom left corner of the board
        x:7,y:7 is the top right of the board
        x is from 0 to 7 (included)
        y is from 0 to 7 (included)
        :param x: the index of rows of the board
        :param y: the index of columns of the board
        """
        self.x = x
        self.y = y

    def get_tuple(self) -> (int, int):
        """
        :return: a tuple of integer x and y
        """
        return self.x, self.y

    def encode(self) -> str:
        """
        The columns are 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'
        The rows are '1', '2', '3', '4', '5', '6', '7', '8'
        An example: Coordinate(0,0) is the bottom left corner of the board. After encoding, it becomes 'a1'.
        :return: coordinate of a square in string type
        """
        return chr(ord('a') + self.y) + str(self.x + 1)

    def __eq__(self, obj: 'Coordinate') -> bool:
        """
        Override the __eq__ function
        :param obj: an object of Coordinate
        :return: True if x and y of the obj are equal to x and y of the self
        """
        return self.x == obj.x and self.y == obj.y

    def __str__(self) -> str:
        """
        Cast Coordinate(x, y) into str "(x, y)".
        :return: "(x, y)".
        """
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self) -> str:
        """
        Cast Coordinate(x, y) into str "(x, y)".
        :return: "(x, y)".
        """
        return "(" + str(self.x) + "," + str(self.y) + ")"

    @staticmethod
    def decode(pos: str) -> 'Coordinate':
        """
        Decode str coordinates into tuple of integer coordinates
        Decode 'a1' -> (0,0)
        :param pos: a str representing a coordinate of board
        :return: an object of Coordinate representing the str coordinates
        """
        return Coordinate(int(pos[1]) - 1, ord(pos[0]) - ord('a'))

    @staticmethod
    def encode_list(lst: ['Coordinate']) -> [str]:
        """
        Encode a list of objects of Coordinates into a list of str coordinates
        Encode [Coordinate(0,0), Coordinate(7,7)] -> ['a1', 'h8']
        :param lst: a list of objects of Coordinates
        :return: a list of str coordinates
        """
        ret = []
        for coord in lst:
            ret.append(coord.encode())
        return ret
