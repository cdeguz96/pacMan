import sys
import pygame as pg
from vector import Vector
from math import fabs, pi, cos, sin

swapped = False
maintainVector = False
li = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
di = {pg.K_RIGHT : Vector(1, 0), pg.K_LEFT : Vector(-1, 0),
      pg.K_UP : Vector(0, -1), pg.K_DOWN : Vector(0, 1)}
epsilon = 0.0001


def compare(a, b): return fabs(a - b) < epsilon

def check_keydown_events(event, character):
    global swapped
    c = character

    if event.key in li and not swapped:
        v, new_dir = c.v, di[event.key]
        if not c.on_star():
            if compare(v.dot(new_dir), -1):
                c.reverse()
            return
        c.v = di[event.key]
        c.choose_next()
        c.scale_factor = c.default_scale_factor
        c.update_angle()

def check_keyup_events(event, character):
    global swapped
    # maintainVector = False
    if event.key in li and swapped:
        character.scale_factor = 0
        swapped = False

def check_events(game):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT: game.finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event=event, character=game.pacman)
            # game.pacman.momentum = True
        elif event.type == pg.KEYUP:
            check_keyup_events(event=event, character=game.pacman)
            # game.pacman.momentum = False
