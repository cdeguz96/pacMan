import pygame as pg
from math import atan2, pi, sin, cos, radians
from vector import Vector
from copy import copy
from timer import Timer, TimerDict


# ===================================================================================================
# class Character
# ===================================================================================================
class Character:
    def __init__(self, game, v, grid_pt, grid_pt_next, grid_pt_prev=None, name='anonymous', scale=1.0, scale_factor=1):
        self.game = game
        self.v = v
        self.maze = game.maze
        self.scale = scale
        self.scale_factor = scale_factor
        self.default_scale_factor = scale_factor
        self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.name = name
        self.rect = None
        self.grid_pt, self.grid_pt_next = grid_pt, grid_pt_next
        self.grid_pt_prev = self.grid_pt
        self.update_next_prev()
        # self.choose_next()
        self.pt = copy(self.grid_pt.pt)
        self.location_displayed = False

    def clamp(self):
        screen = self.screen_rect
        r = self.rect
        self.pt.x = max(-r.width, min(self.pt.x, screen.width + r.width))
        self.pt.y = max(0, min(self.pt.y, screen.height))
        if self.off_screen():
            print(f'{self.name} is off-screen')
            self.grid_pt = self.grid_pt_next
            # self.choose_next()
            self.pt = self.grid_pt.pt
            self.v = Vector(1, 0)
            self.update_next_prev()


    def enterPortal(self): pass

    def at_dest(self):
        delta = (self.pt - self.grid_pt_next.pt).magnitude()
        if delta < 2:
            self.grid_pt = self.grid_pt_next
            self.pt = self.grid_pt.pt
            newdelta = self.pt - self.grid_pt_next.pt
            if not self.location_displayed:
                # print(f'newdelta is: {newdelta} and mag is {newdelta.magnitude()}')
                # print(f'AT DEST {self.grid_pt.index} delta is {delta} pt is {self.pt}, '
                #       f'next is {self.grid_pt_next.pt} with adj_list {self.grid_pt.adj_list}')
                self.location_displayed = True
            return True
        return False

    def at_source(self):
        delta = (self.pt - self.grid_pt_next.pt).magnitude()
        if delta < 2 and delta > 0.1:
            self.pt = self.grid_pt_next.pt
            print(f'AT SOURCE {self.grid_pt.index} with adj_list {self.grid_pt.adj_list}')
            return True
        return False

    def off_screen(self): return self.rect.right < 0 or self.rect.left > self.screen_rect.width

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
        return round((atan2(self.v.x, self.v.y) * 180.0 / pi - 90) % 360, 0)

    def choose_next(self):
        delta = (self.v.x if self.v.y == 0 else -11 * self.v.y)      # -1 left, +1 right, +10 up, -10 down
        grid_pt = self.grid_pt   # current grid point -- where to go next ?
        idx = grid_pt.index
        possible_idx = idx + int(delta)
        if type(self) == 'Pacman':
            print(f'poss_idx {possible_idx} -- Choosing from adj_list for index {self.grid_pt.index} \
                  is {self.grid_pt.adj_list}')
        if idx == 63 or idx == 64:
            print(f"WARNING -- LEAVING GRID possible_idx is {possible_idx}")

        if possible_idx in grid_pt.adj_list:
            self.grid_pt_prev = grid_pt
            self.grid_pt_prev.make_normal()
            idx = self.grid_pt.index
            if possible_idx == 53 or possible_idx == 65:
                print("WARNING -- LEAVING GRID")
            if possible_idx == 65: possible_idx = 55
            if possible_idx == 53: possible_idx = 61
            self.grid_pt_next = self.to_grid(possible_idx)

            self.update_next_prev()
            return True
        return False

    def calc_next(self): return

    def update_angle(self):
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        print(f'ANGLE IS NOW: {curr_angle}')
        # self.image = pg.transform.rotozoom(self.image, delta_angle, 1.0)
        self.image = pg.transform.rotozoom(self.origimage, curr_angle - 90.0, self.scale)
        self.prev_angle = curr_angle


# ===================================================================================================
# class Pacman
# ===================================================================================================
class Pacman(Character):
    images_pman = [pg.image.load('images/pmanopen' + str(x) + '.png') for x in range(0, 12)]

    def __init__(self, game, v=Vector(-1, 0), grid_pt=None):
        super().__init__(game=game, v=v, name="Pacman", scale=0.55, grid_pt=game.maze.location(2, 5),
                         grid_pt_next=game.maze.location(2, 4), scale_factor=3)
        self.image = pg.image.load('images/ship.bmp')
        self.origimage = self.image
        self.prev_angle = 90.0
        self.scale = 0.8
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        self.prev_angle = curr_angle
        print(f'>>>>>>>>>>>>>>>>>>>>>>>> PREV ANGLE is {self.prev_angle}')
        self.last_posn = self.grid_pt
        if self.grid_pt_prev is None: print("PT_PREV IS NONE")
        self.image = pg.transform.rotozoom(self.image, delta_angle, self.scale)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.location_displayed = False
        self.timer = Timer(Pacman.images_pman, wait=20, oscillating=True)
        self.version = 0
        self.step = 1

    def kill_ghost(self): pass
    def eat_point(self): pass
    def eat_fruit(self): pass
    def eat_power_pill(self): pass
    def fire_portal_gun(self, color): pass
    def update(self):
        if self.at_dest():   self.draw();  return
        self.location_displayed = False
        self.pt += self.scale_factor * self.v
        self.clamp()
        if self.grid_pt != self.last_posn:
            self.last_posn = self.grid_pt
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.draw()

    def draw(self):
        angle = self.angle();
        image = self.timer.imagerect()
        image = pg.transform.rotozoom(image, self.angle() + 180, self.scale)
        self.rect = image.get_rect()
        self.rect.centerx, self.rect.centery = self.pt.x + 5, self.pt.y + 5
        self.screen.blit(image, self.rect)


def image_helper(color, direction):
    return [pg.image.load('images/' + color + 'g' + direction + str(x) + '.png') for x in range(3, 5)]


# ===================================================================================================
# class Ghost (base class of all ghosts)
# ===================================================================================================
class Ghost(Character):
    def __init__(self, game, v, grid_pt, grid_pt_next, timer, name="anonymous ghost"):
        super().__init__(game, v=v, grid_pt=grid_pt, grid_pt_next=grid_pt_next, name=name, scale=1.25, scale_factor=1.0)
        self.timer = timer
        self.look_down();
        self.rect = self.timer.imagerect().get_rect()
        self.lasttime = pg.time.get_ticks()
        self.last_posn = self.grid_pt
        self.ghosts = None
        self.count_down = 0
        self.change_every = 5

    def set_ghosts(self, ghosts): self.ghosts = ghosts
    def look_left(self): self.timer.switch_timer('left')
    def look_right(self): self.timer.switch_timer('right')
    def look_up(self): self.timer.switch_timer('up')
    def look_down(self): self.timer.switch_timer('down')
    def look_next(self):
        next = {'left': 'up', 'up': 'right', 'right': 'down', 'down': 'left'}
        thekey = self.timer.getkey()
        nextkey = next[thekey]
        self.timer.switch_timer(nextkey)

    def switch_to_chase(self): pass
    def switch_to_run(self): pass
    def switch_to_flicker(self): pass
    def switch_to_idle(self): pass
    def die(self): pass
    def kill_pacman(self): pass
    def turn(self, dir):
        di = {'straight': 0, 'left': pi / 2.0, 'right': -pi / 2.0, 'reverse': pi}
        angle = di[dir]
        vx_new = round(self.v.x * cos(angle) - self.v.y * sin(angle))
        vy_new = round(self.v.x * sin(angle) + self.v.y * cos(angle))
        self.v = Vector(vx_new, vy_new)

    def set_wait(self, n): self.count_down = n
    def proceed(self): self.count_down -= 1;  return self.count_down == 0
    def occupied(self, grid_pt):
        index = grid_pt.index
        for ghost in self.ghosts:
            print(f'{self.name} at {self.grid_pt.index} going to {self.grid_pt_next.index}')
            if self.name == ghost.name: continue
            if index == ghost.grid_pt_next.index:
                return ghost != self.ghosts[len(self.ghosts) - 1]  # if last ghost, say it's ok to go
        return False

    def calc_next(self, li):
        finished = False
        for direction in li:
            if finished: break
            self.turn(direction)
            finished = self.choose_next()
        print(f'{self.name} is turning {direction} at index {self.grid_pt.index} -- next index {self.grid_pt_next.index}')

    def in_ghost_house(self):
        idx = self.grid_pt.index
        return idx in [59, 60, 61]

    def update(self):
        if self.at_dest(): self.calc_next()
        # print(f'{self.name} at index {self.grid_pt.index}')

        self.pt += self.scale_factor * self.v
        self.clamp()
        if self.grid_pt != self.last_posn:
            self.last_posn = self.grid_pt

        now = pg.time.get_ticks()
        if now - self.lasttime > 3000:
            self.lasttime = now
            self.look_next()
        self.draw()

    def draw(self):
        image = self.timer.imagerect()
        image = pg.transform.rotozoom(image, 0.0, self.scale)
        self.rect = image.get_rect()
        self.rect.centerx, self.rect.centery = self.pt.x + 5, self.pt.y + 5
        self.screen.blit(image, self.rect)


# ===================================================================================================
# class Blinky (red ghost)
# ===================================================================================================
class Blinky(Ghost):
    imagesrl = image_helper(color='r', direction='l')
    imagesrr = image_helper(color='r', direction='r')
    imagesru = image_helper(color='r', direction='u')
    imagesrd = image_helper(color='r', direction='d')

    timer_dict = TimerDict(dict_frames={'left': imagesrl, 'right': imagesrr, 'up': imagesru, 'down': imagesrd},
                           first_key='left')

    def __init__(self, game, v=Vector(-1, 0)):
        super().__init__(game, v=v, grid_pt=game.maze.location(6, 5), grid_pt_next=game.maze.location(6, 4),
                         timer=Blinky.timer_dict, name="Blinky (red ghost)")
        self.look_left()

    def calc_next(self):  super().calc_next(['straight', 'left', 'right', 'reverse'])


# ===================================================================================================
# class Inky (blue ghost)
# ===================================================================================================
class Inky(Ghost):
    imagesbl = image_helper(color='b', direction='l')
    imagesbr = image_helper(color='b', direction='r')
    imagesbu = image_helper(color='b', direction='u')
    imagesbd = image_helper(color='b', direction='d')

    timer_dict = TimerDict(dict_frames = {'left': imagesbl, 'right': imagesbr, 'up': imagesbu, 'down': imagesbd },
                           first_key='left')

    def __init__(self, game, v=Vector(-1, 0)):
        super().__init__(game, v=v, grid_pt=game.maze.location(5, 6),  grid_pt_next=game.maze.location(5, 5),
                         timer=Inky.timer_dict, name="Inky (blue ghost)")
        self.look_left()

    def calc_next(self):  super().calc_next(['right', 'reverse', 'left', 'straight'])


# ===================================================================================================
# class Clyde (orange ghost)
# ===================================================================================================
class Clyde(Ghost):
    imagesol = image_helper(color='o', direction='l')
    imagesor = image_helper(color='o', direction='r')
    imagesou = image_helper(color='o', direction='u')
    imagesod = image_helper(color='o', direction='d')

    timer_dict = TimerDict(dict_frames = {'left': imagesol, 'right': imagesor, 'up': imagesou, 'down': imagesod },
                           first_key='left')

    def __init__(self, game, v=Vector(0, -1)):
        super().__init__(game, v=v, grid_pt=game.maze.location(5, 5),  grid_pt_next=game.maze.location(6, 5),
                         timer=Clyde.timer_dict, name="Clyde (orange ghost)")
        self.look_down()

    def calc_next(self):  super().calc_next(['straight', 'right', 'reverse', 'left'])


# ===================================================================================================
# class Pinky
# ===================================================================================================
class Pinky(Ghost):
    imagespl = image_helper(color='p', direction='l')
    imagespr = image_helper(color='p', direction='r')
    imagespu = image_helper(color='p', direction='u')
    imagespd = image_helper(color='p', direction='d')

    timer_dict = TimerDict(dict_frames = {'left': imagespl, 'right': imagespr, 'up': imagespu, 'down': imagespd},
                           first_key='left')

    def __init__(self, game, v=Vector(1, 0)):
        super().__init__(game, v=v, grid_pt=game.maze.location(5, 4),  grid_pt_next=game.maze.location(5, 5),
                         timer=Pinky.timer_dict, name="Pinky (pink ghost)")
        self.look_right()

    def calc_next(self): super().calc_next(['left', 'right', 'straight', 'reverse'])
