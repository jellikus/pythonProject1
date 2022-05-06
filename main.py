from abc import ABC, abstractmethod
import math
import random
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

# gameIcon = pg.image.load('carIcon.png')
# pg.display.set_icon(gameIcon)

# constants :
WIDTH = 800
HEIGHT = 800
REFRESHRATE = 60
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIECE_COLOR_WHITE = (227, 188, 79)
PIECE_COLOR_DARK = (89, 128, 80)
KING_COLOR = (66, 194, 155)
MOVE_COLOR = (77, 189, 85)

ROWS = 8
COLS = 8
START_BOARD = "1w1w1w1w/w1w1w1w1/1w1w1w1w/8/8/b1b1b1b1/1b1b1b1b/b1b1b1b1"


class GameController:
    def __init__(self, screen, startColor=PIECE_COLOR_WHITE):
        self.screen = screen
        self.selected_troop = None
        self.board = Board(screen)
        self.player_on_turn = startColor

    def select_troop(self, troop):
        if troop == '0':
            return
        if troop

        if not self.selected_troop or troop.color == self.player_on_turn:
            self.selected_troop = troop
            self.visualize_move(self.board.get_moves(troop))

    def select_position(self, idx):
        pass

    def get_troop_valid_moves(self, troop):
        pass

    def get_all_valid_moves(self):
        pass

    def get_valid_moves(self, idx):
        pass

    def make_move(self, idx):
        self.board.make_move(idx, self.selected_troop)

    def change_player_on_turn(self):
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
    def __init__(self, controlKey, exitKey):
        self.controlKey = controlKey
        self.exitKey = exitKey


class AIController:
    pass


class Game:
    def __init__(self, controller):
        self.Controller = controller

    def run(self):
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        game_controller = GameController(screen)
        pg.init()
        pg.display.set_caption('Dáma')
        clock = pg.time.Clock()
        game_controller.board.load_troops(START_BOARD)
        running = True

        # board.make_move((4, 5), board.get_troop_by_idx((0, 1)))
        while running:
            clock.tick(REFRESHRATE)
            running = self.handleEvents(game_controller.board)
            game_controller.board.visualize()
            pg.display.flip()

        pg.quit()

    def handleEvents(self, game_controller):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == self.Controller.exitKey:
                running = False
            elif event.type == self.Controller.controlKey:
                game_controller.select_troop(game_controller.board.get_troop_by_draw_idx(pg.mouse.get_pos()))
                print("troop->", game_controller.board.get_troop_by_draw_idx(pg.mouse.get_pos()))
                print(game_controller.board.get_moves(game_controller.board.get_troop_by_draw_idx(pg.mouse.get_pos())))

        return running


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.board = []
        self.whiteNum = 0
        self.blackNum = 0

    def visualize(self):
        for x in range(0, ROWS):
            for y in range(0, COLS):
                if (x + y) % 2 == 0:
                    pg.draw.rect(self.screen, WHITE,
                                 (x * WIDTH // COLS, y * WIDTH // COLS, WIDTH // COLS, WIDTH // COLS))
        for row in self.board:
            for item in row:
                if item != '0':
                    item.visualize()

    def load_troops(self, boardPositions):
        loadedBoard = parseBoard(boardPositions, ROWS, COLS)
        self.board = loadedBoard
        for x_cord in range(ROWS):
            for y_cord in range(COLS):
                match loadedBoard[x_cord][y_cord]:
                    case 'w':
                        self.whiteNum += 1
                        self.board[x_cord][y_cord] = Piece((x_cord, y_cord), PIECE_COLOR_WHITE, self.screen)
                    case 'b':
                        self.blackNum += 1
                        self.board[x_cord][y_cord] = Piece((x_cord, y_cord), PIECE_COLOR_DARK, self.screen)
                    case 'B':
                        self.blackNum += 1
                        self.board[x_cord][y_cord] = King((x_cord, y_cord), PIECE_COLOR_DARK, self.screen)
                    case 'W':
                        self.whiteNum += 1
                        self.board[x_cord][y_cord] = King((x_cord, y_cord), PIECE_COLOR_WHITE, self.screen)
        for x in self.board:
            print(x)

    def make_move(self, targetIdx, troop):
        if targetIdx == ROWS or 0:
            self.board[troop.x][troop.y] = King((troop.x, troop.y), troop.color, self.screen)
        self.board[troop.x][troop.y], self.board[targetIdx[0]][targetIdx[1]] = self.board[targetIdx[0]][targetIdx[1]], \
                                                                               self.board[troop.x][troop.y]
        troop.set_coordinates(targetIdx)

    def get_troop_by_idx(self, idx):
        return self.board[idx[0]][idx[1]]

    def get_troop_by_draw_idx(self, idx):
        print(idx[0])
        print(idx[1])
        print(idx[0] // (WIDTH // COLS), ",", idx[1] // (WIDTH // COLS))
        return self.board[idx[0] // (WIDTH // COLS)][idx[1] // (WIDTH // COLS)]

    def get_all_troops(self, color):
        pass

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


class ATroop(ABC):
    def __init__(self, position, teamColor, screen):
        self.screen = screen
        self.x = position[0]
        self.y = position[1]
        self.color = teamColor
        self.draw_x = self.draw_y = 0
        self.set_draw_coordinates()

    @abstractmethod
    def visualize(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    def get_draw_coordinates(self):
        return self.x, self.y

    def set_draw_coordinates(self):
        squareSize = WIDTH // ROWS

        self.draw_y = (squareSize // 2) + squareSize * self.y
        self.draw_x = (squareSize // 2) + squareSize * self.x

    def get_coordinates(self):
        return self.x, self.y

    def set_coordinates(self, idx):
        self.x = idx[0]
        self.y = idx[-1]
        self.set_draw_coordinates()


class King(ATroop):
    def visualize(self):
        radius = WIDTH // ROWS // 2 - WIDTH // ROWS // 10
        pg.draw.circle(self.screen, self.color, (self.draw_x, self.draw_y), radius)
        pg.draw.circle(self.screen, BLACK, (self.draw_x, self.draw_y), radius // 2)

    def __repr__(self):
        return f'({self.x}, {self.y}) -> {self.color} King'


class Piece(ATroop):

    def visualize(self):
        radius = WIDTH // ROWS // 2 - WIDTH // ROWS // 10
        pg.draw.circle(self.screen, self.color, (self.draw_x, self.draw_y), radius)

    def __repr__(self):
        if self.color == PIECE_COLOR_WHITE:
            return '\'w\''
        else:
            return '\'d\''
        # return f'({self.x}, {self.y}) -> {self.color} Piece'


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


Game(HumanController(pg.MOUSEBUTTONDOWN, pg.K_ESCAPE)).run()
