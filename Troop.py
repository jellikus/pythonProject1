from Constatnts import *
from abc import ABC, abstractmethod


class ATroop(ABC):
    def __init__(self, position, teamColor, id):
        self.x = position[0]
        self.y = position[1]
        self.color = teamColor
        self.draw_x = self.draw_y = 0
        self.set_draw_coordinates()
        self.id = id

    @abstractmethod
    def visualize(self, screen):
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
    def visualize(self, screen):
        radius = WIDTH // ROWS // 2 - WIDTH // ROWS // 10
        pg.draw.circle(screen, self.color, (self.draw_x, self.draw_y), radius)
        pg.draw.circle(screen, BLACK, (self.draw_x, self.draw_y), radius // 2)

    def __repr__(self):
        # if self.color == PIECE_COLOR_WHITE:
        #     return '\'W\''
        # else:
        #     return '\'D\''
        return f'(K->{self.x},{self.y},id:{self.id})'


class Piece(ATroop):

    def visualize(self, screen):
        radius = WIDTH // ROWS // 2 - WIDTH // ROWS // 10
        pg.draw.circle(screen, self.color, (self.draw_x, self.draw_y), radius)

    def __repr__(self):
        # /  if self.color == PIECE_COLOR_WHITE:
        #       return '\'w\''
        #   else:
        #       return '\'d\''
        return f'(P->{self.x},{self.y},id:{self.id})'
