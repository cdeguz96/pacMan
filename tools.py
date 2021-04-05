import pygame as pg


# Game Fonts
font = "font/Emulogic-zrEw.ttf"

colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (50, 50, 50), 'red': (255, 0, 0),
          'green': (0, 255, 0), 'blue': (0, 0, 255), 'yellow': (255, 255, 0)}

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont = pg.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText