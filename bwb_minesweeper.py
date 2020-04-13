""" A basic Minesweeper game by BWB using Pygame. """

import pygame
from random import randint
from time import time, sleep
from math import ceil


class Game:
    def __init__(self, board_w=10, board_h=10, mines=10):
        self.w = board_w
        self.h = board_h
        self.mine_ct = mines
        self.mine_loc = set()

        self.board = [[Cell(i, j) for j in range(self.h)] for i in range(self.w)]
        self.populate_board()

        [self.win_w, self.win_h] = self.size_window()
        self.start_time = time()

    def size_window(self):
        return (700, 700)

    def populate_board(self):
        # Generate the location of the mines on the boards.
        while len(self.mine_loc) < self.mine_ct:
            self.mine_loc.add((randint(0, self.w), randint(0, self.h)))

        # Place the mines in the board
        for cell in self.board_generator():
            if (cell["x"], cell["y"]) in self.mine_loc:
                cell["obj"].mine = True

    def draw_board(self):
        # TODO: Modify this method to draw timer and flag counter above board
        for cell in self.board_generator():
            cell["obj"].draw()

    def process_move(self, event):
        pass

    @property
    def game_finish(self):
        # LOSE = -1, ONGOING = 0, WIN = 1

        uncovered_cells = 0
        for cell in self.board_generator():
            if cell["obj"].mine and not cell["obj"].covered:
                return -1
            elif not cell["obj"].covered:
                uncovered_cells += 1

        if uncovered_cells == (self.w * self.h) - self.mine_ct:
            return 1
        else:
            return 0

    @property
    def elapsed_time(self):
        return round(time() - self.start_time)

    # A generator for iterating over the gameboard.
    def board_generator(self):
        for y, row in enumerate(self.board):
            for x, obj in enumerate(row):
                yield {"x": x, "y": y, "obj": obj}


class Cell:
    colors = {
        "bg": (195, 191, 184),
        "tl": (250, 250, 250),
        "br": (127, 124, 119),
        "adj": {
            "0": (195, 191, 184),
            "1": (1, 2, 241),
            "2": (0, 128, 26),
            "3": (249, 3, 2),
            "4": (1, 1, 108),
            "5": (125, 0, 0),
            "6": (0, 119, 153),
            "7": (0, 0, 0),
            "8": (122, 119, 114),
        },
        "bge": (189, 189, 189),
        "be": (123, 123, 123),
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mine = False
        self.flagged = False
        self.covered = True

        self.get_coords()

    def get_coords(self):
        self.bg = (self.x * 70, (self.y + 3) * 70, 70, 70)
        self.top = (self.x * 70, (self.y + 3) * 70, 70, ceil(70 / 9))
        self.left = (self.x * 70, (self.y + 3) * 70, ceil(70 / 9), 70)
        self.bottom = (
            self.x * 70,
            ((self.y + 3) * 70) + (70 - ceil(70 / 9)),
            70,
            ceil(70 / 9),
        )
        self.right = (
            (self.x * 70) + (70 - ceil(70 / 9)),
            (self.y + 3) * 70,
            ceil(70 / 9),
            70,
        )

    def draw(self):
        def draw_rect(colors, coords):
            pygame.draw.rect(screen, colors, pygame.Rect(*coords))

        if self.covered:
            draw_rect(self.colors["bg"], self.bg)
            draw_rect(self.colors["tl"], self.top)
            draw_rect(self.colors["tl"], self.left)
            draw_rect(self.colors["br"], self.bottom)
            draw_rect(self.colors["br"], self.right)

        else:
            draw_rect(self.colors["bg"], self.bg)
            draw_rect(self.colors["tl"], self.top)
            draw_rect(self.colors["tl"], self.left)
            draw_rect(self.colors["br"], self.bottom)
            draw_rect(self.colors["br"], self.right)


if __name__ == "__main__":

    g = Game(board_w=10, board_h=10, mines=10)

    screen = pygame.display.set_mode((g.win_w, g.win_h))
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("minesweeper by bwb")

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            g.process_move(event)
            g.draw_board()
            if g.game_finish:
                done = True

        pygame.display.flip()
        clock.tick(60)
