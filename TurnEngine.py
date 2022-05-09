from Troop import *


class MoveMismatch(Exception):
    def __init__(self, from_idx, target_idx):
        self.str = f'{from_idx} to {target_idx}'
        super().__init__(self.str)


class valuesMismatch(Exception):
    pass


class Turn:
    def __init__(self, from_idx, destination, troops_del, board, ):
        self.destination_idx = destination
        self.from_idx = from_idx
        self.troops_to_be_deleted = troops_del
        self.board = board
        self.troop = self.board.get_troop_by_idx((from_idx[0], from_idx[1]))
        self.king_transformation = self._check_king_transformation()
        self.id = id

        # if (troop.x, troop.y) != from_idx:
        #    raise IndexMismatch

    def __repr__(self):
        return f'from: {self.from_idx} to: {self.destination_idx} delete: {self.troops_to_be_deleted}'

    def make_turn(self):
        f_x, f_y = self.from_idx
        d_x, d_y = self.destination_idx

        if self.board.board[f_x][f_y] == '0' or self.board.board[d_x][d_y] != '0':
            raise MoveMismatch(self.board.board[f_x][f_y], self.board.board[d_x][d_y])

        if self.king_transformation:
            self._transform_to_king(f_x, f_y)

        self._delete_troops(self.troops_to_be_deleted)
        self.board.board[f_x][f_y], self.board.board[d_x][d_y] = self.board.board[d_x][d_y], self.board.board[f_x][f_y]
        self.board.board[d_x][d_y].set_coordinates(self.destination_idx)

    def unmake_turn(self):
        f_x, f_y = self.from_idx
        d_x, d_y = self.destination_idx

        if self.king_transformation:
            self._transform_to_piece(d_x, d_y)

        self._add_troops(self.troops_to_be_deleted)
        self.board.board[d_x][d_y], self.board.board[f_x][f_y] = self.board.board[f_x][f_y], self.board.board[d_x][d_y]
        self.board.board[f_x][f_y].set_coordinates(self.from_idx)

    def _check_king_transformation(self):
        f_x, f_y = self.from_idx
        d_x, d_y = self.destination_idx
        if (d_x == ROWS - 1 or d_x == 0) and not isinstance(self.board.board[f_x][f_x], King):
            return True
        return False

    def _transform_to_king(self, f_x, f_y):
        color = self.board.board[f_x][f_y].color
        self.board.board[f_x][f_y] = King((f_x, f_y), color, -self.board.board[f_x][f_y].id)
        self._transform_to_king_count(color)

    def _transform_to_piece(self, d_x, d_y):
        color = self.board.board[d_x][d_y].color
        self.board.board[d_x][d_y] = self.troop
        self._transform_to_piece_count(color)

    def _transform_to_king_count(self, color):
        if color == PIECE_COLOR_WHITE:
            self.board.whiteNum -= 1
            self.board.whiteKingNum += 1
        else:
            self.board.blackNum -= 1
            self.board.blackKingNum += 1

    def _transform_to_piece_count(self, color):
        if color == PIECE_COLOR_WHITE:
            self.board.whiteNum += 1
            self.board.whiteKingNum -= 1
        else:
            self.board.blackNum += 1
            self.board.blackKingNum -= 1

    def _delete_troops(self, troops):
        for troop in troops:
            if self.board.board[troop.x][troop.y] == '0':
                raise valuesMismatch

            self.board.board[troop.x][troop.y] = '0'
            if isinstance(troop, King):
                if troop.color == PIECE_COLOR_DARK:
                    self.board.blackKingNum -= 1
                else:
                    self.board.whiteKingNum -= 1
            else:
                if troop.color == PIECE_COLOR_DARK:
                    self.board.blackNum -= 1
                else:
                    self.board.whiteNum -= 1

    def _add_troops(self, troops):
        for troop in troops:
            if self.board.board[troop.x][troop.y] != '0':
                raise valuesMismatch

            self.board.board[troop.x][troop.y] = troop
            if isinstance(troop, King):
                if troop.color == PIECE_COLOR_DARK:
                    self.board.blackKingNum += 1
                else:
                    self.board.whiteKingNum += 1
            else:
                if troop.color == PIECE_COLOR_DARK:
                    self.board.blackNum += 1
                else:
                    self.board.whiteNum += 1
