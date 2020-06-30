import pygame as pg
import numpy as np
from settings import *



class g_map(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = [game.map_group,game.all_sprites]
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((WIDTH - 40, HEIGHT- 40))
        self.image.fill(BLACK)
        self.rect = pg.Rect(20,20,WIDTH - 40,HEIGHT - 40)

    def get_mouse(self,event):
        pass
