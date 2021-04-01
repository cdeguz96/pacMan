import pygame as pg
import game_functions as gf
from settings import Settings
from maze import Maze, GridPoint
from character import Pacman, Blinky, Inky, Pinky, Clyde


# ===================================================================================================
# class Game
# ===================================================================================================
class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("PacMan Portal")
        self.font = pg.font.SysFont(None, 48)

        self.maze = Maze(game=self)

        self.pacman = Pacman(game=self)
        self.ghosts = [Blinky(game=self), Pinky(game=self), Clyde(game=self), Inky(game=self)]
        for ghost in self.ghosts:
            ghost.set_ghosts(self.ghosts)
        self.finished = False

    def to_grid(self, index):
        row = index // 11
        offset = index % 11
        ss = self.maze.location(row, offset)
        return ss

    def to_pixel(self, grid): pixels = []

    def play(self):
        while not self.finished:
            gf.check_events(game=self)
            # self.screen.fill(self.settings.bg_color)
            self.maze.update()
            for ghost in self.ghosts: ghost.update()
            self.pacman.update()
            pg.display.flip()


def main():
    game = Game()
    game.play()


if __name__ == '__main__': main()

