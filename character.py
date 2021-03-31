import pygame as pg
from math import atan2
from copy import copy
from vector import Vector
from timer import Timer
from settings import Settings


class Character:
    def __init__(self, game, v, grid_pt, grid_pt_next, grid_pt_prev, name, filename, scale):
        self.game = game
        self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.name = name
        self.grid_pt, self.grid_pt_next, self.grid_pt_prev = grid_pt, grid_pt_next, grid_pt_prev

        pt_next = self.grid_pt_next.pt
        self.pt = copy(self.grid_pt.pt)
        delta = pt_next - self.pt
        v = delta.normalize()

        self.grid_pt_next.make_next()
        self.grid_pt_prev.make_prev()

        self.image = pg.image.load('images/' + filename)
        self.scale = scale
        self.origimage = self.image
        self.scale_factor = 1.0
        self.v = v
        self.prev_angle = 90.0
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        self.prev_angle = curr_angle
        print(f'>>>>>>>>>>>>>>>>>>>>>>>> PREV ANGLE is {self.prev_angle}')
        self.last = self.grid_pt
        if self.grid_pt_prev is None: print("PT_PREV IS NONE NONE NONE NONE NONE")
        self.image = pg.transform.rotozoom(self.image, delta_angle, scale)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.printed = False

    def clamp(self):
        screen = self.screen_rect
        self.pt.x = max(0, min(self.pt.x, screen.width))
        self.pt.y = max(0, min(self.pt.y, screen.height))

    def enterPortal(self): pass

    def at_dest(self):
        delta = (self.pt - self.grid_pt_next.pt).magnitude()
        if delta < 2:
            self.grid_pt = self.grid_pt_next
            self.pt = self.grid_pt.pt
            newdelta = self.pt - self.grid_pt_next.pt
            if not self.printed:
                print(f'newdelta is: {newdelta} and mag is {newdelta.magnitude()}')
                print(f'AT DEST {self.grid_pt.index} delta is {delta} pt is {self.pt}, next is {self.grid_pt_next.pt} with adj_list {self.grid_pt.adj_list}')
                self.printed = True
            return True
        return False

    def at_source(self):
        delta = (self.pt - self.grid_pt_next.pt).magnitude()
        if delta < 2 and delta > 0.1:
            self.pt = self.grid_pt_next.pt
            print(f'AT SOURCE {self.grid_pt.index} with adj_list {self.grid_pt.adj_list}')
            return True
        return False

    def on_star(self):
        return self.at_dest() or self.at_source()

    def to_grid(self, index):
        return self.game.to_grid(index)

    def update_next_prev(self):
        self.grid_pt_next.make_next()
        self.grid_pt_prev.make_visited()

    def reverse(self):
        temp = self.grid_pt_prev
        self.grid_pt_prev = self.grid_pt_next
        self.grid_pt_next = temp

        self.grid_pt_prev.make_prev()
        self.grid_pt_next.make_next()

        self.v *= -1
        self.scale_factor = 1
        self.update_angle()

    def angle(self):
        return round((atan2(self.v.x, self.v.y) * 180.0 / 3.1415 - 90) % 360, 0)
        # return atan2(self.v.x, self.v.y) * 180.0 / 3.1415 + 180.0

    def update_angle(self):
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        # self.image = pg.transform.rotozoom(self.image, delta_angle, 1.0)
        self.image = pg.transform.rotozoom(self.origimage, curr_angle - 90.0, self.scale)
        self.prev_angle = curr_angle

    def update(self):
        # print(f'{self.pt} with dims={self.pt.dims} and {self.pt_next} with dims={self.pt.dims}')
        delta = self.pt - self.grid_pt_next.pt
        # print(f'         delta is: {delta} and mag is {delta.magnitude()}')
        if self.at_dest():   self.draw();  return

        print(f'changing location... --- with velocity {self.v}')
            # print(f'current {self.grid_pt}... --- next {self.grid_pt_next}')
            # self.prev = self.grid_pt
        self.printed = False
        self.pt += self.scale_factor * self.v
        self.clamp()
        if self.grid_pt != self.last:
            # print(f'{self.name}@{self.pt} -- next is: {self.grid_pt_next}')
            self.last = self.grid_pt
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.draw()

    def draw(self): self.screen.blit(self.image, self.rect)


class Pacman(Character):
    def __init__(self, game, v, grid_pt, grid_pt_next, grid_pt_prev, name="Pacman", filename="ship.bmp", scale=0.55):
        super().__init__(game=game, name=name, filename=filename, scale=scale,
                         v=v, grid_pt=grid_pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev)

    def killGhost(self): pass
    def eatPoint(self): pass
    def eatFruit(self): pass
    def eatPowerPill(self): pass
    def firePortalGun(self, color): pass
    # def update(self):  self.draw()

    # def draw(): pass


class Ghost(Character):
    def __init__(self, game, v, grid_pt, grid_pt_next, grid_pt_prev, name="Pinky", filename="alien10.png", scale=0.8):
        super().__init__(game, v=v, grid_pt=grid_pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev, name=name,
                         filename=filename, scale=scale)

    def switchToChase(self): pass
    def switchToRun(self): pass
    def switchToFlicker(self): pass
    def switchToIdle(self): pass
    def die(self): pass
    def killPacman(self): pass
    # def update(self):  self.draw()

    # def draw(): pass
