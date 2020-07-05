import pygame as pg
import numpy as np
import random as r
from camera import *
from settings import *

class g_map(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = [game.map_group,game.all_sprites]
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.map_camera = camera()
        self.map_camera.y = 2330
        self.states = [False,False,False,False]

        self.pointer_img = self.game.pointer
        self.image = pg.transform.scale(game.map_bg,(1920,WORLD_MAP_HEIGHT))
        self.rect = pg.Rect(0,0,WIDTH,HEIGHT)
        self.original_rect = pg.Rect(0,0,WIDTH,HEIGHT)

        self.make_planets()
        self.image.blit(self.pointer_img,(100,100))

    def make_planets(self):
        'PLANET STUFF'
        self.planet_imgs = []
        self.planet_scales = []
        self.planet_pos = [] #decided first
        last_column = 0
        columns = 0
        randomness = 200

        self.planet_pos.append([WIDTH/2,-WORLD_MAP_HEIGHT/(2*LAYERS) + (LAYERS)*WORLD_MAP_HEIGHT/LAYERS]) #first planet
        'FIRST 3 PLANETS'
        for i in range(3):
            self.planet_pos.append([960+200*(i -1),-randomness/2+r.randrange(randomness)-WORLD_MAP_HEIGHT/(2*LAYERS) + (LAYERS-1)*WORLD_MAP_HEIGHT/LAYERS]) #first planet
        self.planet_pos.append([WIDTH/2,WORLD_MAP_HEIGHT/(2*LAYERS)]) #last planet
        for layer in range(2,LAYERS-1):
            while columns == last_column:
                columns = r.randrange(4,LAYER_WIDTH+1)
            last_column = columns
            for column in range(columns):
                self.planet_pos.append([960+200*(column - (columns-1)/2),-randomness/2+r.randrange(randomness)-WORLD_MAP_HEIGHT/(2*LAYERS) + layer*WORLD_MAP_HEIGHT/LAYERS])
        for planet_position in self.planet_pos:
            self.planet_imgs.append(self.game.planets[r.randrange(6)].copy())
            self.planet_scales.append(r.uniform(1,2))
        for i in range(len(self.planet_imgs)):
            self.planet_imgs[i] = pg.transform.scale(self.planet_imgs[i],(int(20*self.planet_scales[i]),int(20*self.planet_scales[i])))
            self.planet_imgs[i] = self.get_outline(self.planet_imgs[i],WHITE)
            self.image.blit(self.planet_imgs[i],(self.planet_pos[i][0],self.planet_pos[i][1]))

    def update(self):
        self.map_camera.update(self.states)
        self.rect = self.map_camera.apply_rect(self.original_rect)

    def get_outline(self,image,color=(0,0,0)):
        rect = image.get_rect()
        mask = pg.mask.from_surface(image)
        outline = mask.outline()
        outline_image = pg.Surface(rect.size).convert_alpha()
        outline_image.fill((0,0,0,0))
        for point in outline:
            outline_image.set_at(point,color)

        merged = image.copy()
        merged.blit(outline_image, (0, 0))

        return merged

    def get_mouse(self,event):
        pass
