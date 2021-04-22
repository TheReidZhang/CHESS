import copy
from api.piece.coordinate import Coordinate
from colorama import Fore, Style
from api.piece.piece_interface import Color


class SimpleAI:
    def __init__(self, game: 'ChessGame'):
        self.game = game
        self.values = {"p": 1, "P": 1,
                       "n": 3, "N": 3,
                       "b": 3, "B": 3,
                       "r": 5, "R": 5,
                       "q": 9, "Q": 9,
                       "k": 0, "K": 0,
                       "*": 0}
        self.board_value = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0],
            [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0],
            [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0],
            [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def get_value(self, board):
        ret = 0
        for row in range(8):
            for col in range(8):
                if board[row][col].get_color() != self.game.turn:
                    ret -= self.values[board[row][col].to_string()]
                else:
                    ret += self.board_value[row][col]
        return ret

    def get_next_move(self):
        board = copy.deepcopy(self.game.board)
        src_row, src_col, tar_row, tar_col = 0, 0, 0, 0
        max_score = -10000
        for row in range(8):
            for col in range(8):
                moves = self.game.get_checked_moves(Coordinate(row,col))["moves"]
                for coordinate in moves:
                    r1, c1 = Coordinate.decode(coordinate).get_tuple()
                    src_piece = board[row][col]
                    tar_piece = board[r1][c1]
                    board[r1][c1] = src_piece
                    board[row][col] = self.game.empty_cell
                    ret = self.get_value(board)
                    if ret > max_score:
                        src_row, src_col, tar_row, tar_col = row, col, r1, c1
                        max_score = ret
                    board[row][col] = src_piece
                    board[r1][c1] = tar_piece

        return src_row, src_col, tar_row, tar_col
