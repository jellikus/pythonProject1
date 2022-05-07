from Constatnts import *
import math
import copy


class HeurisitcWhite:

    def troops_and_row(self, board):
        pass

    def troops(self, board):
        return board.whiteNum - board.blackNum

    def troops_king(self, board):
        return board.whiteNum + 2 * board.whiteKingNum - board.blackNum - 2 * board.blackKingNum


class HeurisitcBlack:

    def troops_and_row(self, board):
        pass

    def troops(self, board):
        return board.blackNum - board.whiteNum

    def troops_king(self, board):
        return board.blackNum + 2 * board.blackKingNum - board.whiteNum - 2 * board.whiteKingNum


class AI:
    def __init__(self, board, heuristic, color=PIECE_COLOR_WHITE):
        self.board = board
        self.heuristic = heuristic
        self.color = color

    def search(self, depth, alpha, beta):
        if depth == 0:
            return self.heuristic.troops_king(self.board)

        moves = self.generateMoves()  # get all possible moves

        if len(moves) == 0:
            return 0

        bestEval = -math.inf

        for move in moves:
            idx = (move[0].x, move[0].y)
            self.ai_make_move(move[0], move[1])
            search_val = - self.search(depth - 1, 0, 0)
            bestEval = max(search_val, bestEval)
            self.ai_unmake_move(move[0], idx, move[2])

        return bestEval

    def generateMoves(self):
        moves = []
        # d = [move for troop in self.board.get_troops_by_color(self.color) for move in self.board.get_moves(troop).items() or []]

        for troop in self.board.get_troops_by_color(self.color):
            for move in self.board.get_moves(troop).items():
                if move[1]:
                    moves.append((troop, move[0], copy.deepcopy(self.board.get_troop_by_idx(move[1][0], move[1][1]))))
                else:
                    moves.append((troop, move[0], []))

        return moves

    def ai_make_move(self, troop, idx):
        self.board.make_move(idx, troop)

    def ai_unmake_move(self, troop, idx, deletedList):
        self.board.make_move(idx, troop)
        if deletedList:
            for troop in deletedList:
                self.board[troop.x][troop.y] = troop
