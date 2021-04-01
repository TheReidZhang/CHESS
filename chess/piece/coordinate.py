class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_tuple(self):
        return self.x, self.y

    def encode(self):
        return chr(ord('a') + self.y) + str(self.x + 1)

    def __eq__(self, obj):
        return self.x == obj.x and self.y == obj.y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    @staticmethod
    def decode(pos: str) -> tuple:
        return Coordinate(int(pos[1]) - 1, ord(pos[0]) - ord('a'))

    @staticmethod
    def encode_list(lst: list) -> list:
        ret = []
        for coord in lst:
            ret.append(coord.encode())
        return ret
