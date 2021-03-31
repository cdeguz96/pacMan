import pygame as pg
from copy import copy
import game_functions as gf
from settings import Settings
from vector import Vector
from maze import Maze, GridPoint
from character import Pacman, Ghost
from math import atan2
from timer import Timer
import time

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("PacMan Portal")
        self.font = pg.font.SysFont(None, 48)

        self.maze = Maze(game=self)

        nxt = self.maze.location(5, 8)
        grid_pt = self.maze.location(3, 8)
        prev = self.maze.location(2, 8)

        # nxt = self.stars5[8]
        # grid_pt = self.stars3[8]
        # prev = self.stars2[8]

        self.pacman = Pacman(game=self, v=Vector(-1, 0), grid_pt=grid_pt, grid_pt_next=nxt, grid_pt_prev=prev)
        # self.ghost = Ghost(game=self)

        # self.grid = self.create_grid()
        self.finished = False

    def to_grid(self, index):
        row = index // 11
        offset = index % 11
        ss = self.maze.location(row, offset)
        return ss

    def to_pixel(self, grid):
        pixels = []

    def play(self):
        while not self.finished:
            gf.check_events(game=self)
            # self.screen.fill(self.settings.bg_color)
            self.maze.update()
            # self.ghost.update()
            self.pacman.update()
            pg.display.flip()

def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

