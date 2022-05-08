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
        return board.whiteNum + 2 * board.whiteKingNum - board.blackNum - 2 * board.blackKingNum


class HeurisitcBlack:
    def __init__(self):
        self.color = PIECE_COLOR_DARK

    def troops_and_row(self, board):
        pass

    def troops(self, board):
        return board.blackNum - board.whiteNum

    def troops_king(self, board):
        return board.blackNum + 2 * board.blackKingNum - board.whiteNum - 2 * board.whiteKingNum


class AI:
    def __init__(self, board, heuristic):
        self.board = board
        self.heuristic = heuristic
        self.color = heuristic.color
        self.bestMove = None

    def search(self, depth, alpha, beta):
        if depth == 0:
            return self.heuristic.troops_king(self.board), None

        moves = self.generateMoves()  # get all possible moves

        if len(moves) == 0:
            return (0, None)

        best_move = None
        bestEval = -math.inf

        #print(f'ALL MOVES:', moves)
        for move in moves:
            idx = (move[0].x, move[0].y)

            #print(f' BEFORE making move from {idx} to {move[1]} in depth: {depth}')
            self.ai_make_move(move[0], move[1], move[2])

            search_val = - self.search(depth - 1, 0, 0)[0]
            bestEval = max(search_val, bestEval)

            if bestEval == search_val:
                best_move = move

            #print(f'making back move from {(move[0].x, move[0].y)} to {idx} in depth: {depth}')
            self.ai_unmake_move(move[0], idx, move[2])

        return bestEval, best_move

    def generateMoves(self):
        moves = []
        # d = [move for troop in self.board.get_troops_by_color(self.color) for move in self.board.get_moves(troop).items() or []]

        for troop in self.board.get_troops_by_color(self.color):
            for move in self.board.get_moves(troop).items():
                if move[1]:
                    moves.append((troop, move[0], copy.deepcopy(move[1])))
                else:
                    moves.append((troop, move[0], []))

        return moves

    def ai_make_move(self, troop, idx, deletedList):
        self.board.make_move(idx, troop)
        if deletedList:
            for troop in deletedList:
                self.board.board[troop.x][troop.y] = troop
                if troop.__class__.__name__ == 'King':
                    if troop.color == PIECE_COLOR_WHITE:
                        self.board.blackKingNum -= 1
                    else:
                        self.board.whiteKingNum -= 1
                else:
                    if troop.color == PIECE_COLOR_WHITE:
                        self.board.blackNum -= 1
                    else:
                        self.board.whiteNum -= 1

            return

    def ai_unmake_move(self, troop, idx, deletedList):
        self.board.board[idx[0]][idx[1]] = troop
        self.board.board[troop.x][troop.y] = '0'
        troop.set_coordinates(idx)
        if deletedList:
            for troop in deletedList:
                self.board.board[troop.x][troop.y] = troop
                if troop.__class__.__name__ == 'King':
                    if troop.color == PIECE_COLOR_WHITE:
                        self.board.blackKingNum += 1
                    else:
                        self.board.whiteKingNum += 1
                else:
                    if troop.color == PIECE_COLOR_WHITE:
                        self.board.blackNum += 1
                    else:
                        self.board.whiteNum += 1

            return


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pg.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pg.display.update()
