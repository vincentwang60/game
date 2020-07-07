import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (60, 60, 60)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (41,16,38)
BLUE = (0,0,255)
BLUE2 = (30, 55, 153)
DARKBLUE = (9, 28, 76)
GREY1 = (60, 99, 130)
BLUE3 = (10, 61, 98)
LIGHTBLUE = (106, 137, 204)
POWER_COLOR = (241, 196, 15)
MINERALS_COLOR = (230, 126, 34)
RESEARCH_COLOR = (52, 152, 219)
BASE_COLOR = (231, 76, 60)
UNKNOWN_COLOR = (149, 165, 166)
HULL_COLOR = (230, 126, 34)

# map galaxy
LAYERS = 10
LAYER_WIDTH = 6
WORLD_MAP_HEIGHT = 3412
LINK_DISTANCE = 300

# game settings
FONT_NAME = "Calibri"
font_name = pg.font.match_font(FONT_NAME)
BUTTON_X = 2
BUTTON_Y = 2
BUTTON_W = 68
BUTTON_H = 18
WIDTH = 1920
HEIGHT = 1080
SEPARATION = 20 #distance that ships have to stay apart
BEAM_RANGE = 500
BEAM_DURATION = 20
SCROLL_SPEED = 20
FPS = 60
STAR_DENSITY = 0.0001
MAP_SIZE = (3000,3000)
TITLE = "Vincent's Game"
BGCOLOR = PURPLE
