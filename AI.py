from Constatnts import *
import math
import copy
from TurnEngine import Turn


class HeurisitcWhite:
    def __init__(self):
        self.color = PIECE_COLOR_WHITE

    def troops_and_row(self, board):
        pass

    def troops(self, board):
        return board.whiteNum - board.blackNum

    def troops_king(self, board):
        # print(board.whiteNum, "+1.5*", board.whiteKingNum,"-" , board.blackNum ,"-1.5*", board.blackKingNum )
        return board.whiteNum + 1.2 * board.whiteKingNum - board.blackNum - 1.2 * board.blackKingNum


class HeurisitcBlack:
    def __init__(self):
        self.color = PIECE_COLOR_DARK

    def troops_and_row(self, board):
        pass

    def troops(self, board):
        return board.blackNum - board.whiteNum

    def troops_king(self, board):
        return board.blackNum + 1.2 * board.blackKingNum - board.whiteNum - 1.2 * board.whiteKingNum


class AI:
    def get_opposite_color(self):
        if self.color == PIECE_COLOR_WHITE:
            return PIECE_COLOR_DARK
        else:
            return PIECE_COLOR_WHITE

    def __init__(self, board, heuristic):
        self.board = board
        self.heuristic = heuristic
        self.color = heuristic.color
        self.bestMove = None
        self.nodesExpanded = 0
        self.depth_now = 0

    def run_minmax(self, depth, alpha, beta):
        value = self.search_max(depth, alpha, beta)
        computedMove = self.bestMove
        self.bestMove = None
        return value, computedMove

    def search_max(self, depth, alpha, beta):

        if depth == 0:
            x = self.heuristic.troops_king(self.board)
            return x

        if self.board.blackNum == 0 and self.board.blackKingNum == 0 or self.board.whiteNum == 0 and self.board.whiteKingNum == 0:
            if self.color == PIECE_COLOR_WHITE:
                return (self.board.whiteNum + self.board.whiteKingNum) - (
                        self.board.blackKingNum + self.board.blackNum) * 500 + (
                               self.board.whiteNum + self.board.whiteKingNum) * 50
            else:
                return (self.board.blackNum + self.board.blackKingNum) - (
                        self.board.whiteKingNum + self.board.whiteNum) * 500 + (
                               self.board.blackNum + self.board.blackKingNum) * 50

        bestEval = -math.inf
        for troop, target, to_delete in self.generateMoves(self.color):

            turn = Turn((troop.x, troop.y), target, to_delete, self.board)
            turn.make_turn()

            search_val = self.search_min(depth - 1, alpha, beta)

            if search_val > bestEval:
                bestEval = search_val
                if depth == AI_SEARCH_DEPTH:
                    print("BEST eval", bestEval, "move: ",
                          turn)

                    self.bestMove = turn

            turn.unmake_turn()

            if bestEval >= beta:
                return bestEval
            alpha = max(alpha, bestEval)

        return bestEval

    def search_min(self, depth, alpha, beta):
        if depth == 0:
            x = self.heuristic.troops_king(self.board)
            return x

        if self.board.blackNum == 0 and self.board.blackKingNum == 0 or self.board.whiteNum == 0 and self.board.whiteKingNum == 0:
            if self.color == PIECE_COLOR_WHITE:
                return (self.board.whiteNum + self.board.whiteKingNum) - (
                        self.board.blackKingNum + self.board.blackNum) * 500 + (
                               self.board.whiteNum + self.board.whiteKingNum) * 50
            else:
                return (self.board.blackNum + self.board.blackKingNum) - (
                        self.board.whiteKingNum + self.board.whiteNum) * 500 + (
                               self.board.blackNum + self.board.blackKingNum) * 50

        bestEval = math.inf
        for troop, target, to_delete in self.generateMoves(self.get_opposite_color()):

            # if self.board.board[troop.x][troop.y] == '0':
            #     pass

            # print("check:", troop, target, to_delete)
            # print(self.board.board[troop.x][troop.y], self.board.board[target[0]][target[1]])
            turn = Turn((troop.x, troop.y), target, to_delete, self.board)
            turn.make_turn()

            search_val = self.search_max(depth - 1, alpha, beta)
            # print("min_search_val:", search_val, " depth: ", depth, "white: ", self.board.whiteNum, ",",
            #       self.board.whiteKingNum, " balck: ", self.board.blackNum, ",", self.board.blackKingNum, "move: ",
            #       turn)

            if search_val < bestEval:
                bestEval = search_val

            turn.unmake_turn()

            if bestEval <= alpha:
                self.depth_now -= 1
                return bestEval
            beta = min(beta, bestEval)

        return bestEval

    def generateMoves(self, color):
        moves = []
        for troop in self.board.get_troops_by_color(color):
            for move in self.board.get_moves(troop).items():
                if move[1]:
                    moves.append((troop, move[0], move[1]))
                else:
                    moves.append((troop, move[0], []))

        moves.sort(key=lambda emp: len(emp[2]), reverse=True)
        return moves
