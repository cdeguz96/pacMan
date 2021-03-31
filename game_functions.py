import sys
import pygame as pg
from vector import Vector
from math import fabs

swapped = False
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
        # choose next star for destination
        v = di[event.key]
        delta = (v.x if v.y == 0 else -11 * v.y)      # -1 left, +1 right, +10 up, -10 down
        grid_pt = c.grid_pt   # current grid point -- where to go next ?
        idx = grid_pt.index
        possible_idx = idx + int(delta)
        print(f'poss_idx {possible_idx} -- Choosing from adj_list for index {c.grid_pt.index} is {c.grid_pt.adj_list}')
        if possible_idx in grid_pt.adj_list:
            # c.grid_pt_next = possible_idx
            c.grid_pt_prev.make_normal()

            c.grid_pt_next = c.to_grid(possible_idx)
            c.grid_pt_prev = grid_pt
            c.update_next_prev()
        c.v = di[event.key]
        c.scale_factor = 1.0
        c.update_angle()

def check_keyup_events(event, character):
    global swapped
    if event.key in li and swapped:
        character.scale_factor = 0
        swapped = False
    # if event.key == pg.K_q: ship.shooting_bullets = False

# def check_play_button(stats, play_button, mouse_x, mouse_y):
#     if play_button.rect.collidepoint(mouse_x, mouse_y):
#         stats.game_active = True

def check_events(game):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT: game.finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            # check_play_button(stats=game.stats, play_button=game.play_button, mouse_x=mouse_x, mouse_y=mouse_y)
        elif event.type == pg.KEYDOWN: check_keydown_events(event=event, character=game.pacman)
        elif event.type == pg.KEYUP: check_keyup_events(event=event, character=game.pacman)

