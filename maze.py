import pygame as pg
from timer import Timer
from vector import Vector
from settings import Settings

xlocs = {0: 70, 1: 120, 2: 210, 3: 310, 4: 400, 5: 450, 6: 500, 7: 590, 8: 690, 9: 780, 10: 830 }
COLUMNS = 11

def helper(n, li): return (n, xlocs[n % 11], li)

def LR(n): return helper(n, [n - 1, n + 1])
def UD(n): return helper(n, [n - COLUMNS, n + COLUMNS])

def L(n):  return helper(n, [n + 1, n + COLUMNS])
def R(n):  return helper(n, [n - 1, n + COLUMNS])
def gL(n): return helper(n, [n - COLUMNS, n + 1])
def gR(n): return helper(n, [n - COLUMNS, n - 1])

def T(n):   return helper(n, [n - COLUMNS, n - 1, n + 1])
def TL(n):  return helper(n, [n - COLUMNS, n + 1, n + COLUMNS])
def TR(n):  return helper(n, [n - COLUMNS, n - 1, n + COLUMNS])
def TUD(n): return helper(n, [n - 1, n + 1, n + COLUMNS])

def cross(n):  return helper(n, [n - COLUMNS, n - 1, n + 1, n + COLUMNS])
def wrapL(n):  return helper(n, [n + 1, n + COLUMNS - 1])
def wrapR(n):  return helper(n, [n - 1,  n - COLUMNS])
def Lonly(n):  return helper(n, [n - 1])
def Ronly(n):  return helper(n, [n + 1])
def Null(n):   return helper(n, [])


def id(row, x): return COLUMNS * row + x


def stars9(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [gL(id(r, 0)), LR(id(r, 1)), T(id(r, 2)), LR(id(r, 3)), gR(id(r, 4)),
                                        Null(id(r, 5)), gL(id(r, 6)), LR(id(r, 7)), T(id(r, 8)), LR(id(r, 9)),
                                        gR(id(r, 10))]]

def stars8(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [TL(id(r, 0)), LR(id(r, 1)), cross(id(r, 2)), T(id(r, 3)), TUD(id(r, 4)),
                                         LR(id(r, 5)), TUD(id(r, 6)), T(id(r, 7)), cross(id(r, 8)), LR(id(r, 9)),
                                         TR(id(r, 10))]]

def stars7(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [L(id(r, 0)), LR(id(r, 1)), TR(id(r, 2)), L(id(r, 3)), gR(id(r, 4)),
                                         Null(id(r, 5)), gL(id(r, 6)), R(id(r, 7)), TL(id(r, 8)), LR(id(r, 9)),
                                         R(id(r, 10))]]

def stars6(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [Null(id(r, 0)), Null(id(r, 1)), UD(id(r, 2)), gL(id(r, 3)), TUD(id(r, 4)),
                                         T(id(r, 5)), TUD(id(r, 6)), gR(id(r, 7)), UD(id(r, 8))]]

def stars5(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [wrapL(id(r, 0)), LR(id(r, 1)), cross(id(r, 2)), TR(id(r, 3)), Ronly(id(r, 4)),
                                         TUD(id(r, 5)), Lonly(id(r, 6)), TL(id(r, 7)),
                                         cross(id(r, 8)), LR(id(r, 9)), wrapR(id(r, 10))]]

def stars4(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [Null(id(r, 0)), Null(id(r, 1)), UD(id(r, 2)), TL(id(r, 3)), LR(id(r, 4)),
                                         LR(id(r, 5)), LR(id(r, 6)), TR(id(r, 7)), UD(id(r, 8))]]

def stars3(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [gL(id(r, 0)), LR(id(r, 1)), cross(id(r, 2)), TUD(id(r, 3)), gR(id(r, 4)),
                                         Null(id(r, 5)), gL(id(r, 6)), TUD(id(r, 7)), cross(id(r, 8)), LR(id(r, 9)),
                                         gR(id(r, 10))]]

def stars2(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [L(id(r, 0)), gR(id(r, 1)), TL(id(r, 2)), T(id(r, 3)), TUD(id(r, 4)),
                                         LR(id(r, 5)), TUD(id(r, 6)), T(id(r, 7)), TR(id(r, 8)), gL(id(r, 9)),
                                         R(id(r, 10))]]

def stars1(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [gL(id(r, 0)), TUD(id(r, 1)), R(id(r, 2)), L(id(r, 3)), gR(id(r, 4)),
                                         Null(id(r, 5)), gL(id(r, 6)), R(id(r, 7)), L(id(r, 8)), TUD(id(r, 9)),
                                         gR(id(r, 10))]]

def stars0(game, row_index, y):
    r = row_index
    return [GridPoint(game=game, pt=Vector(x, y), index=index, adj_list=adj_list)
            for (index, x, adj_list) in [L(id(r, 0)), LR(id(r, 1)), LR(id(r, 2)), LR(id(r, 3)), TUD(id(r, 4)),
                                         LR(id(r, 5)), TUD(id(r, 6)), LR(id(r, 7)), LR(id(r, 8)), LR(id(r, 9)),
                                         R(id(r, 10))]]

class Maze:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.image = pg.image.load('images/maze.png')
        self.image = pg.transform.rotozoom(self.image, 0, 0.6)
        self.rect = self.image.get_rect()

        self.stars0 = stars0(game=self, row_index=0, y=925)
        self.stars1 = stars1(game=self, row_index=1, y=835)
        self.stars2 = stars2(game=self, row_index=2, y=735)
        self.stars3 = stars3(game=self, row_index=3, y=641)

        self.stars4 = stars4(game=self, row_index=4, y=541)
        self.stars5 = stars5(game=self, row_index=5, y=445)
        self.stars6 = stars6(game=self, row_index=6, y=350)
        self.stars7 = stars7(game=self, row_index=7, y=255)
        self.stars8 = stars8(game=self, row_index=8, y=160)
        self.stars9 = stars9(game=self, row_index=9, y=70)

        self.grid = [self.stars0, self.stars1, self.stars2, self.stars3, self.stars4, self.stars5, self.stars6,
                     self.stars7, self.stars8, self.stars9]

    def location(self, row, col): return self.grid[row][col]

    def update(self):
        self.draw()
        for stars in self.grid:
            for star in stars:
                star.update()

    def draw(self): self.screen.blit(self.image, self.rect)


class GridPoint:
    image0 = pg.image.load('images/star.png')
    image0 = pg.transform.rotozoom(image0, 0, 0.7)
    image1 = pg.transform.rotozoom(image0, 0, 1.1)
    image2 = pg.transform.rotozoom(image0, 0, 1.2)
    image3 = pg.transform.rotozoom(image0, 0, 1.3)
    images = [image0, image1, image2, image3, image2, image1]

    imagen0 = pg.image.load('images/star_next.png')
    imagen0 = pg.transform.rotozoom(imagen0, 0, 0.7)
    imagen1 = pg.transform.rotozoom(imagen0, 0, 1.1)
    imagen2 = pg.transform.rotozoom(imagen0, 0, 1.2)
    imagen3 = pg.transform.rotozoom(imagen0, 0, 1.3)
    imagesn = [imagen0, imagen1, imagen2, imagen3, imagen2, imagen1]

    imagep0 = pg.image.load('images/star_prev.png')
    imagep0 = pg.transform.rotozoom(imagep0, 0, 0.7)
    imagep1 = pg.transform.rotozoom(imagep0, 0, 1.1)
    imagep2 = pg.transform.rotozoom(imagep0, 0, 1.2)
    imagep3 = pg.transform.rotozoom(imagep0, 0, 1.3)
    imagesp = [imagep0, imagep1, imagep2, imagep3, imagep2, imagep1]

    imagev0 = pg.image.load('images/star_visited.png')
    imagev0 = pg.transform.rotozoom(imagev0, 0, 0.7)
    imagev1 = pg.transform.rotozoom(imagev0, 0, 1.1)
    imagev2 = pg.transform.rotozoom(imagev0, 0, 1.2)
    imagev3 = pg.transform.rotozoom(imagev0, 0, 1.3)
    imagesv = [imagev0, imagev1, imagev2, imagev3, imagev2, imagev1]


    def __init__(self, game, pt=Vector(70,931), index=0, adj_list=[]):
        self.game = game
        self.screen = game.screen
        self.pt = pt
        self.index = index
        self.adj_list = adj_list
        self.timer_normal = Timer(GridPoint.images, wait=100)
        self.timer_visited = Timer(GridPoint.imagesv, wait=100)
        self.timer_next = Timer(GridPoint.imagesn, wait=100)
        self.timer_prev = Timer(GridPoint.imagesp, wait=100)
        self.timer = self.timer_normal

    def update(self): self.draw()

    def make_next(self): self.timer = self.timer_next

    def make_prev(self): self.timer = self.timer_prev

    def make_normal(self): pass    #  self.timer = self.timer_normal

    def make_visited(self): self.timer = self.timer_visited

    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.centerx, rect.centery = self.pt.x, self.pt.y
        self.screen.blit(image, rect)
