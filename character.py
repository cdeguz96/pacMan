import pygame as pg
import game_functions as gf
from math import atan2, pi, sin, cos, radians
from vector import Vector
from copy import copy
from timer import Timer, TimerDict


# ===================================================================================================
# class Character
# ===================================================================================================
class Character:
    def __init__(self, game, v, grid_pt, grid_pt_next, grid_pt_prev=None, name='anonymous', scale=1.0, scale_factor=1.0):
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
        self.pt = copy(self.grid_pt.pt)

    def clamp(self):
        screen = self.screen_rect
        r = self.rect
        self.pt.x = max(-r.width, min(self.pt.x, screen.width + r.width))
        self.pt.y = max(0, min(self.pt.y, screen.height))
        if self.off_screen():
            self.grid_pt = self.grid_pt_next
            self.pt = self.grid_pt.pt

    def enterPortal(self): pass

    def at_dest(self):
        delta = (self.pt - self.grid_pt_next.pt).magnitude()
        if delta < 2:
            self.grid_pt = self.grid_pt_next
            self.pt = self.grid_pt.pt
            newdelta = self.pt - self.grid_pt_next.pt
            return True
        return False

    def at_source(self):
        delta = (self.pt - self.grid_pt_next.pt).magnitude()
        if delta < 2 and delta > 0.1:
            self.pt = self.grid_pt_next.pt
            return True
        return False

    def off_screen(self): return self.rect.right < 0 or self.rect.left > self.screen_rect.width

    def on_star(self):
        return self.at_dest() or self.at_source()

    def to_grid(self, index):
        return self.game.to_grid(index)

    def reverse(self):
        temp = self.grid_pt_prev
        self.grid_pt_prev = self.grid_pt_next
        self.grid_pt_next = temp

        self.v *= -1
        self.update_angle()

    def angle(self):
        return round((atan2(self.v.x, self.v.y) * 180.0 / pi - 90) % 360, 0)

    def choose_next(self):
        delta = (self.v.x if self.v.y == 0 else -11 * self.v.y)         # -1 left, +1 right, +10 up, -10 down
        grid_pt = self.grid_pt                                          # current grid point -- where to go next ?
        idx = grid_pt.index
        possible_idx = idx + int(delta)

        if possible_idx in grid_pt.adj_list:
            self.grid_pt_prev = grid_pt
            idx = self.grid_pt.index
            if possible_idx == 65: possible_idx = 56
            if possible_idx == 55: possible_idx = 64
            self.grid_pt_next = self.to_grid(possible_idx)

            return True
        return False

    def calc_next(self): return

    def update_angle(self):
        curr_angle = self.angle()
        # delta_angle = curr_angle - self.prev_angle
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
        self.image = self.images_pman[0] #pg.image.load('images/ship.bmp')
        self.origimage = self.image
        self.prev_angle = 90.0
        self.scale = 0.8
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        self.prev_angle = curr_angle
        self.last_posn = self.grid_pt
        self.image = pg.transform.rotozoom(self.image, delta_angle, self.scale)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.timer = Timer(Pacman.images_pman, wait=20, oscillating=True)

    def reset(self):

        self.v = Vector(-1, 0)
        self.grid_pt = self.game.maze.location(2, 5)
        self.grid_pt_next = self.game.maze.location(2, 4)
        self.last_posn = self.grid_pt
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.grid_pt_prev = self.grid_pt
        self.pt = copy(self.grid_pt.pt)

    def check_ghost_collisions(self, ghost):
        if self.rect.colliderect(ghost.rect):
            if self.game.ghostsRunning:
                self.kill_ghost(ghost)
            else:
                ghost.kill_pacman()
                self.reset()

    def check_item_collision(self, grid_pt):
        if grid_pt.eaten: return
        if self.rect.collidepoint(grid_pt.pt.x, grid_pt.pt.y):
            if grid_pt.type == 'point':
                self.eat_point()
            if grid_pt.type == 'power':
                self.eat_power_pill()
        grid_pt.update()

    def kill_ghost(self, ghost):
        self.game.stats.score += 500
        ghost.ghost_reset()

    def eat_point(self):
        if not self.grid_pt.eaten:
            self.grid_pt.eaten = True
            self.game.stats.score += 100

    def eat_fruit(self): pass

    def eat_power_pill(self):
        self.grid_pt.eaten = True
        self.game.ghostsRunning = True
        self.game.startGhostRun = pg.time.get_ticks()

    def fire_portal_gun(self, color): pass

    def update(self):
        self.check_item_collision(self.grid_pt_next)
        if self.at_dest():
            self.draw()
            return
        self.pt += self.scale_factor * self.v
        self.clamp()
        if self.grid_pt != self.last_posn:
            self.last_posn = self.grid_pt
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.draw()

    def draw(self):
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
    bg1 = pg.image.load('images/bg3.png')
    bg2 = pg.image.load('images/bg4.png')
    wg1 = pg.image.load('images/wg3.png')
    wg2 = pg.image.load('images/wg4.png')

    imagesRunning = [bg1, bg2]
    imagesFlicker = [bg1, wg1, bg2, wg2]

    def __init__(self, game, v, grid_pt, grid_pt_next, timer, name="anonymous ghost"):
        super().__init__(game, v=v, grid_pt=grid_pt, grid_pt_next=grid_pt_next, name=name, scale=1.25, scale_factor=1.0)
        self.timer = timer
        self.look_down()
        self.rect = self.timer.imagerect().get_rect()
        self.lasttime = pg.time.get_ticks()
        self.last_posn = self.grid_pt
        self.ghosts = None
        self.count_down = 0
        self.change_every = 5

        self.startRunning = None
        self.running = False
        self.timerRunning = Timer(Ghost.imagesRunning)

        self.startFlicker = None
        self.flicker = False
        self.timerFlicker = Timer(Ghost.imagesFlicker)



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

    # def switch_to_chase(self): pass
    def switch_to_run(self):
        self.running = True
        self.startRunning = pg.time.get_ticks()


    def switch_to_flicker(self):
        self.flicker = True
        self.startFlicker = pg.time.get_ticks()

    def switch_to_idle(self): pass

    def ghost_reset(self):
        self.grid_pt = self.game.maze.location(5, 6)
        self.grid_pt_next = self.game.maze.location(5, 5)
        self.v = Vector(-1, 0)
        self.pt = copy(self.grid_pt.pt)

    def kill_pacman(self):
        for ghost in self.game.ghosts:
            ghost.ghost_reset()
        self.game.stats.lives_left -= 1

        if self.game.stats.lives_left <= 0:
            self.game.start_over()

    def turn(self, dir):
        di = {'straight': 0, 'left': pi / 2.0, 'right': -pi / 2.0, 'reverse': pi}
        angle = di[dir]
        vx_new = round(self.v.x * cos(angle) - self.v.y * sin(angle))
        vy_new = round(self.v.x * sin(angle) + self.v.y * cos(angle))
        self.v = Vector(vx_new, vy_new)

    def set_wait(self, n): self.count_down = n
    def proceed(self): self.count_down -= 1; return self.count_down == 0
    
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
        # print(f'{self.name} is turning {direction} at index {self.grid_pt.index} -- next index {self.grid_pt_next.index}')

    def in_ghost_house(self):
        idx = self.grid_pt.index
        return idx in [59, 60, 61]

    def update(self):
        if self.at_dest(): self.calc_next()
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
        if self.game.ghostsRunning and not self.game.ghostsFlicker:
            image = self.timerRunning.imagerect()
        elif self.game.ghostsFlicker:
            image = self.timerFlicker.imagerect()
        else:
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
