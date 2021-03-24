class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def decode(pos: str) -> tuple:
        pass

    @staticmethod
    def encode(pos: tuple) -> str:
        pass
