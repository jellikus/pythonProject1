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

ROWS = 8
COLS = 8
START_BOARD = "1w1w1w1w/w1w1w1w1/1w1w1w1w/8/8/b1b1b1b1/1b1b1b1b/b1b1b1b1"


class Game:
    def __init__(self):
        pass

    def run(self):

        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.init()
        pg.display.set_caption('Dáma')
        clock = pg.time.Clock()
        board = Board([], 0, 0, SCREEN)
        board.load_troops(START_BOARD)
        running = True

        board.make_move((5, 5), board.get_troop_by_idx((0, 1)))

        while running:
            clock.tick(REFRESHRATE)
            running = self.handleEvents(board)
            board.visualize()
            pg.display.flip()

        pg.quit()

    def handleEvents(self, board):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                print(board.get_troop_by_draw_idx(pg.mouse.get_pos()))
        return running


class Board:
    def __init__(self, troopPositions, whiteNum, blackNum, screen):
        self.screen = screen
        self.board = []
        self.whiteNum = whiteNum
        self.blackNum = blackNum

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
        print(idx[0] // (WIDTH // COLS),",", idx[1] // (WIDTH // COLS))
        return self.board[idx[0] // (WIDTH // COLS)][idx[1] // (WIDTH // COLS)]


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
        return f'({self.x}, {self.y}) -> {self.color} Piece'


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


Game().run()
