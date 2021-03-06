import pygame as pg
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
START_COLOR = PIECE_COLOR_WHITE
ROWS = 5
COLS = 5
AI_SEARCH_DEPTH = 17

#START_BOARD = "1w1w1w1w/w1w1w1w1/1w1w1w1w/8/8/b1b1b1b1/1b1b1b1b/b1b1b1b1"
#START_BOARD = "1w1w1w1w/w1w1w1w1/8/8/8/8/1b1b1b1b/b1b1b1b1"
#START_BOARD = "5w2/b3w1w1/7w/2w5/7b/4b3/1W5w/4b1b1"
START_BOARD = "1w1w1/5/5/5/1b1b1"
#START_BOARD = "3w1/w4/5/4b/1b3"
#START_BOARD = "5/w3w/3b1/5/1b3"