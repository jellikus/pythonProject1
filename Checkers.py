import os
from AI import AI, HeurisitcBlack, HeurisitcWhite
from Troop import *
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from TurnEngine import Turn
import math

# gameIcon = pg.image.load('carIcon.png')
# pg.display.set_icon(gameIcon)

class GameController:

    def __init__(self, screen, startColor=PIECE_COLOR_WHITE):
        self.screen = screen
        self.selected_troop = None
        self.board = Board(screen)
        self.player_on_turn = startColor
        self.possible_moves = {}
        self.selectPhase = True
        self.turn_history = []

    def get_turn_back(self):
        if self.turn_history:
            self.turn_history.pop().unmake_turn()
            self.change_player_on_turn()

    def select_troop(self, troop):
        if troop == '0':
            self.selectPhase = True
            self.possible_moves = {}
            return

        if troop.color == self.player_on_turn:
            self.selected_troop = troop
            self.possible_moves = self.board.get_moves(troop)
            self.selectPhase = False
            return

        self.selectPhase = False
        self.possible_moves = {}

    def select_target_pos(self, destination_idx, delete_troops):
        turn = Turn((self.selected_troop.x, self.selected_troop.y), destination_idx, delete_troops, self.board)
        self.turn_history.append(turn)
        turn.make_turn()
        self.possible_moves = {}
        self.selectPhase = True

    def get_winner(self):
        if self.board.whiteNum + self.board.whiteKingNum == 0:
            return PIECE_COLOR_DARK
        if self.board.blackNum + self.board.blackKingNum == 0:
            return PIECE_COLOR_WHITE
        return None

    def get_troop_valid_moves(self, troop):
        pass

    def get_all_valid_moves(self):
        pass

    def get_valid_moves(self, idx):
        pass

    def make_move(self, idx):
        self.board.make_move(idx, self.selected_troop)

    def change_player_on_turn(self):
        # print("white:", self.board.whiteNum, "+", self.board.whiteKingNum, " black", self.board.blackNum, "+",
        #      self.board.blackKingNum)

        if self.player_on_turn == PIECE_COLOR_WHITE:
            self.player_on_turn = PIECE_COLOR_DARK
        else:
            self.player_on_turn = PIECE_COLOR_WHITE

    def visualize_move(self, move_list):
        radius = WIDTH // ROWS // 2 - WIDTH // ROWS // 10
        squareSize = WIDTH // ROWS
        for m in move_list:
            draw_y = (squareSize // 2) + squareSize * m[1]
            draw_x = (squareSize // 2) + squareSize * m[0]
            pg.draw.circle(self.screen, MOVE_COLOR, (draw_x, draw_y), radius // 4)


class HumanController:
    def __init__(self, controlKey, exitKey, historyKey):
        self.controlKey = controlKey
        self.exitKey = exitKey
        self.historyKey = historyKey


class AIController:
    pass


class Game:
    def __init__(self, controller):
        self.Controller = controller

    def visualize_game(self, game_controller):
        game_controller.board.visualize()
        game_controller.visualize_move(game_controller.possible_moves)

    def run(self):
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        game_controller = GameController(screen, START_COLOR)
        ai_controller_white = AI(game_controller.board, HeurisitcWhite())
        ai_scontroller_black = AI(game_controller.board, HeurisitcBlack())
        # ai_controller = None

        pg.init()
        pg.display.set_caption('Draughts')
        clock = pg.time.Clock()
        game_controller.board.load_troops(START_BOARD)
        running = True

        # board.make_move((4, 5), board.get_troop_by_idx((0, 1)))
        while running:
            clock.tick(REFRESHRATE)
            running = self.handleEvents(game_controller, ai_controller_white, ai_scontroller_black)
            self.visualize_game(game_controller)
            pg.display.flip()

            if game_controller.get_winner():
                print(f'winner is {game_controller.get_winner()}!')
                break

        pg.quit()

    def handleEvents(self, game_controller, ai_controller_1=None, ai_controller_2=None):
        running = True
        if ai_controller_1 and ai_controller_1.color == game_controller.player_on_turn:
            value, move = ai_controller_1.run_minmax(AI_SEARCH_DEPTH, -math.inf, +math.inf)
            print("EVAL:", value, move)
            print("---------------------------------------------------------------------------------------------------")
            move.make_turn()
            game_controller.turn_history.append(move)
            game_controller.change_player_on_turn()

        elif ai_controller_2 and ai_controller_2.color == game_controller.player_on_turn:
            value, move = ai_controller_2.run_minmax(AI_SEARCH_DEPTH, -math.inf, +math.inf)
            print("EVAL:", value, move)
            print("---------------------------------------------------------------------------------------------------")
            move.make_turn()
            game_controller.turn_history.append(move)
            game_controller.change_player_on_turn()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == self.Controller.exitKey:
                running = False
            elif event.type == pg.KEYDOWN and event.key == self.Controller.historyKey:
                game_controller.get_turn_back()
            elif event.type == self.Controller.controlKey:
                if game_controller.selectPhase:
                    game_controller.select_troop(game_controller.board.get_troop_by_draw_idx(pg.mouse.get_pos()))
                else:
                    pos = game_controller.board.convert_draw_idx(pg.mouse.get_pos())
                    if pos in game_controller.possible_moves:
                        game_controller.select_target_pos(pos, game_controller.possible_moves[pos])
                        print(game_controller.board.blackKingNum, " ", game_controller.board.blackNum, " ",
                              game_controller.board.whiteKingNum, " ", game_controller.board.whiteNum)
                        game_controller.change_player_on_turn()
                    else:
                        game_controller.selectPhase = True
                        game_controller.possible_moves = {}

                # print("troop->", game_controller.board.get_troop_by_draw_idx(pg.mouse.get_pos()))
                # print(game_controller.board.get_moves(game_controller.board.get_troop_by_draw_idx(pg.mouse.get_pos())))

        return running



class Board:
    def __init__(self, screen):
        self.screen = screen
        self.board = []
        self.whiteNum = 0
        self.blackNum = 0
        self.whiteKingNum = 0
        self.blackKingNum = 0

    def visualize(self):
        for x in range(0, ROWS):
            for y in range(0, COLS):
                if (x + y) % 2 == 0:
                    pg.draw.rect(self.screen, WHITE,
                                 (x * WIDTH // COLS, y * WIDTH // COLS, WIDTH // COLS, WIDTH // COLS))
                else:
                    pg.draw.rect(self.screen, BLACK,
                                 (x * WIDTH // COLS, y * WIDTH // COLS, WIDTH // COLS, WIDTH // COLS))
        for row in self.board:
            for item in row:
                if item != '0':
                    item.visualize(self.screen)

    def load_troops(self, boardPositions):
        loadedBoard = parseBoard(boardPositions, ROWS, COLS)
        self.board = loadedBoard
        num = 0
        for x_cord in range(ROWS):
            for y_cord in range(COLS):
                match loadedBoard[x_cord][y_cord]:
                    case 'w':
                        self.whiteNum += 1
                        num += 1
                        self.board[x_cord][y_cord] = Piece((x_cord, y_cord), PIECE_COLOR_WHITE, num)
                    case 'b':
                        self.blackNum += 1
                        num += 1
                        self.board[x_cord][y_cord] = Piece((x_cord, y_cord), PIECE_COLOR_DARK,num)
                    case 'B':
                        self.blackKingNum += 1
                        num += 1
                        self.board[x_cord][y_cord] = King((x_cord, y_cord), PIECE_COLOR_DARK, num)
                    case 'W':
                        self.whiteKingNum += 1
                        num += 1
                        self.board[x_cord][y_cord] = King((x_cord, y_cord), PIECE_COLOR_WHITE, num)

    def addKing(self, color):
        if color == PIECE_COLOR_WHITE:
            self.whiteNum -= 1
            self.whiteKingNum += 1
        else:
            self.blackNum -= 1
            self.blackKingNum += 1

    def make_move(self, targetIdx, troop):
        if (targetIdx[0] == ROWS - 1 or targetIdx[0] == 0) and not isinstance(troop, King):
            self.board[troop.x][troop.y] = King((targetIdx[0], targetIdx[1]), troop.color)
            self.addKing(troop.color)

        self.board[troop.x][troop.y], self.board[targetIdx[0]][targetIdx[1]] = self.board[targetIdx[0]][targetIdx[1]], \
                                                                               self.board[troop.x][troop.y]
        troop.set_coordinates(targetIdx)

    def get_troop_by_idx(self, idx):
        return self.board[idx[0]][idx[1]]

    def get_troop_by_draw_idx(self, idx):
        return self.board[idx[0] // (WIDTH // COLS)][idx[1] // (WIDTH // COLS)]

    def convert_draw_idx(self, idx):
        return (idx[0] // (WIDTH // COLS)), (idx[1] // (WIDTH // COLS))

    def get_troops_by_color(self, color):
        lst = []
        for x in range(ROWS):
            for y in range(COLS):
                if self.board[x][y] != '0' and self.board[x][y].color == color:
                    lst.append(self.board[x][y])
        return lst

    def get_moves(self, piece):
        moves = {}
        left = piece.y - 1
        right = piece.y + 1
        row = piece.x

        if piece.color == PIECE_COLOR_DARK or isinstance(piece, King):
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == PIECE_COLOR_WHITE or isinstance(piece, King):
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == '0':
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == '0':
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves


def parseBoard(str, rws, col):
    foo = []  # Final board
    pieces = str.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []  # This is the row I make
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('0')
            else:
                foo2.append(thing)
        foo.append(foo2)

    if len(foo) != rws:
        raise IndexError
    for z in foo:
        if len(z) != col:
            raise IndexError
    return foo


Game(HumanController(pg.MOUSEBUTTONDOWN, pg.K_ESCAPE, pg.K_h)).run()
