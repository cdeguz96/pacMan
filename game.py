import pygame as pg
import game_functions as gf
from settings import Settings
from maze import Maze, GridPoint
from character import Pacman, Blinky, Inky, Pinky, Clyde
from game_stats import GameStats
from tools import font, colors, text_format

# import text
# import os

# ===================================================================================================
# class Game
# ===================================================================================================

class Game:
    def __init__(self):
        pg.init()

        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))

        self.main_menu()
        self.maze = Maze(game=self)
        self.stats = GameStats(self)

        self.pacman = Pacman(game=self)
        self.ghosts = [Blinky(game=self), Pinky(game=self), Clyde(game=self), Inky(game=self)]
        for ghost in self.ghosts:
            ghost.set_ghosts(self.ghosts)
        self.finished = False
        # self.score = 0

        self.ghostsRunning = False
        self.startGhostRun = None
        self.ghostsFlicker = False

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
            if self.maze.complete:
                self.level_up() #send ghost home # level up #reset maze
            for ghost in self.ghosts:
                self.pacman.check_ghost_collisions(ghost)
                ghost.update()
            self.pacman.update()
            if self.ghostsRunning:
                self.check_ghost_run()
            self.stats.display_stats()
            pg.display.flip()

    # *****************************

    def level_up(self):
        self.stats.level += 1
        self.maze.reset()
        for ghost in self.ghosts:
            ghost.ghost_reset()
            ghost.scale_factor *= 1.1

        self.pacman.reset()
        self.pacman.scale_factor *= 1.1

    def start_over(self):
        self.maze.reset()
        self.stats.reset_stats()
        for ghost in self.ghosts:
            ghost.ghost_reset()
        self.pacman.reset()

    def check_ghost_run(self):
        now = pg.time.get_ticks()
        if now - self.startGhostRun > 12000 and not self.ghostsFlicker:
            self.ghostsFlicker = True

        if self.ghostsFlicker:
            if now - self.startGhostRun > 15000:
                self.ghostsRunning = False
                self.ghostsFlicker = False

    # Main Menu
    def main_menu(self):
        menu = True
        selected = "start"

        while menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = "start"
                    elif event.key == pg.K_DOWN:
                        selected = "quit"
                    if event.key == pg.K_RETURN:
                        if selected == "start":
                            return
                        if selected == "quit":
                            pg.quit()
                            quit()

            # Main Menu UI
            self.screen.fill(colors['blue'])
            title = text_format("PacMan", font, 65, colors['yellow'])
            if selected == "start":
                text_start = text_format("START", font, 45, colors['white'])
            else:
                text_start = text_format("START", font, 45, colors['black'])
            if selected == "quit":
                text_quit = text_format("QUIT", font, 45, colors['white'])
            else:
                text_quit = text_format("QUIT", font, 45, colors['black'])

            title_rect = title.get_rect()
            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()

            # Main Menu Text
            self.screen.blit(title, (self.settings.screen_width / 2 - (title_rect[2] / 2), 80))
            self.screen.blit(text_start, (self.settings.screen_width / 2 - (start_rect[2] / 2), 300))
            self.screen.blit(text_quit, (self.settings.screen_width / 2 - (quit_rect[2] / 2), 360))
            pg.display.update()
            # clock.tick(FPS)
            pg.display.set_caption("PacMan Portal")
# ***************************************************


def main():
    game = Game()
    game.play()


if __name__ == '__main__': main()


