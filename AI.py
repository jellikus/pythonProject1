from Constatnts import *
import pygame as pg
import math
import copy


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
        value = copy.deepcopy(self.search_max(depth, alpha, beta))
        computedMove = self.bestMove
        self.bestMove = None
        return value, computedMove

    def search_max(self, depth, alpha, beta):

        if depth == 0:
            x = self.heuristic.troops_king(self.board)
            return x

        if self.board.blackNum == 0 and self.board.blackKingNum == 0 or self.board.whiteNum == 0 and self.board.whiteKingNum == 0:
            print("max:WINNER")
            return (self.board.whiteNum + self.board.whiteKingNum) - (
                    self.board.blackKingNum + self.board.blackNum) * 500 + (
                           self.board.whiteNum + self.board.whiteKingNum) * 50

        bestEval = -math.inf
        for move in self.generateMoves(self.color):

            boardCopy = copy.deepcopy(self.board.board)
            wk = copy.deepcopy(self.board.whiteKingNum)
            w = copy.deepcopy(self.board.whiteNum)
            dk = copy.deepcopy(self.board.blackKingNum)
            d = copy.deepcopy(self.board.blackNum)
            mv = copy.deepcopy(move)

            self.ai_make_move(move[0], move[1], move[2])

            search_val = self.search_min(depth - 1, alpha, beta)
            print("max_search_val:", search_val, " depth: ", depth, "white: ", self.board.whiteNum, ",",
                  self.board.whiteKingNum, " balck: ", self.board.blackNum, ",", self.board.blackKingNum, "move: ",
                  mv)

            if search_val > bestEval:
                bestEval = search_val
                if depth == AI_SEARCH_DEPTH:
                    print("BEST eval", bestEval, "move: ",
                          move)

                    self.bestMove = mv

            self.board.board = boardCopy
            self.board.whiteKingNum = wk
            self.board.whiteNum = w
            self.board.blackKingNum = dk
            self.board.blackNum = d

            if bestEval >= beta:
                return bestEval
            alpha = max(alpha, bestEval)

            # self.ai_unmake_move(troopCopy, idx, move[2], move[0].x, move[0].y)
            # print("white: ", self.board.whiteNum, ",", self.board.whiteKingNum, " balck: ",
            #     self.board.blackNum, ",", self.board.blackKingNum, "to be backuped:", deleteList)
        return bestEval

    def search_min(self, depth, alpha, beta):
        if depth == 0:
            x = self.heuristic.troops_king(self.board)
            return x

        if self.board.blackNum == 0 and self.board.blackKingNum == 0 or self.board.whiteNum == 0 and self.board.whiteKingNum == 0:
            print("max:WINNER")
            return (self.board.whiteNum + self.board.whiteKingNum) - (
                    self.board.blackKingNum + self.board.blackNum) * 500 + (
                           self.board.whiteNum + self.board.whiteKingNum) * 50

        bestEval = math.inf

        mvs = self.generateMoves(self.color)
        for move in self.generateMoves(self.get_opposite_color()):

            boardCopy = copy.deepcopy(self.board.board)
            wk = copy.deepcopy(self.board.whiteKingNum)
            w = copy.deepcopy(self.board.whiteNum)
            dk = copy.deepcopy(self.board.blackKingNum)
            d = copy.deepcopy(self.board.blackNum)
            mv = copy.deepcopy(move)

            self.ai_make_move(move[0], move[1], move[2])

            search_val = self.search_max(depth - 1, alpha, beta)
            print("min_search_val:", search_val, " depth: ", depth, "white: ", self.board.whiteNum, ",",
                  self.board.whiteKingNum, " balck: ", self.board.blackNum, ",", self.board.blackKingNum, "move: ",
                  mv)
            if search_val < bestEval:
                bestEval = search_val

            self.board.board = boardCopy
            self.board.whiteKingNum = wk
            self.board.whiteNum = w
            self.board.blackKingNum = dk
            self.board.blackNum = d

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

    def ai_make_move(self, troop_move, idx, deletedList):
        self.board.make_move(idx, troop_move)
        if deletedList:
            for troop in deletedList:
                self.board.board[troop.x][troop.y] = '0'
                if troop.__class__.__name__ == 'King':
                    if troop.color == PIECE_COLOR_DARK:
                        self.board.blackKingNum -= 1
                    else:
                        self.board.whiteKingNum -= 1
                else:
                    if troop.color == PIECE_COLOR_DARK:
                        self.board.blackNum -= 1
                    else:
                        self.board.whiteNum -= 1
            return

    def ai_unmake_move(self, troop_move, idx, deletedList, x, y):
        self.board.board[idx[0]][idx[1]] = troop_move
        self.board.board[x][y] = '0'
        troop_move.set_coordinates(idx)
        if deletedList:
            for troop in deletedList:
                self.board.board[troop.x][troop.y] = troop
                if troop.__class__.__name__ == 'King':
                    if troop.color == PIECE_COLOR_DARK:
                        self.board.blackKingNum += 1
                    else:
                        self.board.whiteKingNum += 1
                else:
                    if troop.color == PIECE_COLOR_DARK:
                        self.board.blackNum += 1
                    else:
                        self.board.whiteNum += 1
            return
