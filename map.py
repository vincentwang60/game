import pygame as pg
import numpy as np
import random as r
from camera import *
from settings import *

class planet(pg.sprite.Sprite):
    def __init__(self,x,y,layer_x,layer_y,image):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.layer_x = layer_x
        self.layer_y = layer_y
        self.image = image
        self.resources = ['power','minerals','research','base','unknown']
        self.resource = self.resources[r.randrange(5)]
        random = r.uniform(1,2)
        self.original_image = image.copy()
        self.original_image.fill((r.randrange(50), r.randrange(50), r.randrange(50), 100), special_flags=pg.BLEND_SUB)
        self.original_image = pg.transform.rotate(self.original_image,r.randrange(360))
        self.image = pg.transform.scale(self.original_image,(int(20*random),int(20*random)))
        self.image = self.get_outline(self.image)
        self.center = tuple((self.x+20*random/2,self.y+20*random/2))
        self.linked = []
        self.rect = pg.Rect(int(self.x),int(self.y),30,30)

    def connected_to_next(self):
        for link in self.linked:
            if link[1] == self.layer_y + 1:
                return True
        return False

    def get_outline(self,image):
        if self.resource == 'power':
            color = POWER_COLOR
        if self.resource == 'minerals':
            color = MINERALS_COLOR
        if self.resource == 'research':
            color = RESEARCH_COLOR
        if self.resource == 'base':
            color = BASE_COLOR
        if self.resource == 'unknown':
            color = UNKNOWN_COLOR
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

class g_map(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = [game.map_group,game.all_sprites]
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.map_camera = camera()
        self.map_camera.y = 2330
        self.states = [False,False,False,False]
        self.planets = []
        self.layer_width = [1,3]
        self.current_planet = None

        self.pointer_img = self.game.pointer
        self.image = pg.transform.scale(game.map_bg,(1920,WORLD_MAP_HEIGHT))
        self.map_bg = pg.transform.scale(game.map_bg,(1920,WORLD_MAP_HEIGHT))
        self.rect = pg.Rect(0,0,WIDTH,HEIGHT)
        self.original_rect = pg.Rect(0,0,WIDTH,HEIGHT)

        self.make_planets()
        self.make_links()
        self.draw_links()
        self.draw_planets()
        self.image.blit(self.pointer_img,(self.current_planet.center[0]-45,self.current_planet.center[1]-53))

    def make_planets(self):
        'PLANET STUFF'
        self.planet_scales = []
        last_column = 0
        columns = 0
        randomness = 200 #y deviation
        distance = 250 #width between planet

        self.current_planet = planet(WIDTH/2,-WORLD_MAP_HEIGHT/(2*LAYERS) + (LAYERS)*WORLD_MAP_HEIGHT/LAYERS,0,0,self.game.planets[r.randrange(6)])
        self.planets.append(self.current_planet) #create first planet
        'FIRST 3 PLANETS'
        for i in range(3):
            self.planets.append(planet(960+1.5*distance*(i -1)-randomness/4+r.randrange(randomness/2),-randomness/2+r.randrange(randomness)-WORLD_MAP_HEIGHT/(2*LAYERS) + (LAYERS-1)*WORLD_MAP_HEIGHT/LAYERS,i,1,self.game.planets[r.randrange(6)]))
        'LAST 3 PLANETS'
        for i in range(3):
            self.planets.append(planet(960+1.5*distance*(i -1)-randomness/4+r.randrange(randomness/2),-randomness/2+r.randrange(randomness)-WORLD_MAP_HEIGHT/(2*LAYERS) + (2)*WORLD_MAP_HEIGHT/LAYERS,i,8,self.game.planets[r.randrange(6)]))
        self.planets.append(planet(WIDTH/2,WORLD_MAP_HEIGHT/(2*LAYERS),0,LAYERS-1,self.game.planets[r.randrange(6)])) #last planet

        for layer in range(3,LAYERS-1):
            while columns == last_column:
                columns = r.randrange(4,LAYER_WIDTH+1)
            last_column = columns
            self.layer_width.append(columns)
            for column in range(columns):
                self.planets.append(planet(960+distance*(column - (columns-1)/2)-randomness/4+r.randrange(randomness/2),-randomness/2+r.randrange(randomness)-WORLD_MAP_HEIGHT/(2*LAYERS) + layer*WORLD_MAP_HEIGHT/LAYERS,column,LAYERS-layer,self.game.planets[r.randrange(6)]))
        self.layer_width.append(3)
        self.layer_width.append(1)
        self.layer_width.reverse()

    def draw_planets(self):
        for planet_i in self.planets:
            self.image.blit(planet_i.image,(planet_i.x,planet_i.y))

    def make_links(self):
        current_layer = 0
        for next_layer in range(1,LAYERS):
            current_layer_list = [] #list of planets in current layer
            next_layer_list = [] #list of planets in next layer
            current_layer = next_layer - 1
            for planet in self.planets:
                if planet.layer_y == current_layer:
                    current_layer_list.append(planet)
                if planet.layer_y == next_layer:
                    next_layer_list.append(planet)
            for current_planet in current_layer_list:
                for next_planet in next_layer_list:
                    if (current_planet.layer_x == 0 and next_planet.layer_x == 0) or (current_planet.layer_x == self.layer_width[current_layer]-1 and next_planet.layer_x == self.layer_width[next_layer]-1):
                        self.make_link(current_planet,next_planet)

            #randomly connects planets if they're close enough
            for current_planet in current_layer_list:
                for next_planet in next_layer_list:
                    if abs(current_planet.x - next_planet.x) < 200:
                        self.make_link(current_planet,next_planet)
            for planet in next_layer_list:
                if len(planet.linked)==0: #if a planet in the next layer has no connections
                    min_distance = 1000
                    min_planet = None
                    for current_planet in current_layer_list:
                        if abs(current_planet.x - planet.x) < min_distance:
                            min_distance = abs(current_planet.x-planet.x)
                            min_planet = current_planet
                    self.make_link(min_planet,planet)
            for planet in current_layer_list:
                if not planet.connected_to_next(): #if a planet in the current layer has no connections
                    min_distance = 1000
                    min_planet = None
                    for next_planet in next_layer_list:
                        if abs(next_planet.x - planet.x) < min_distance:
                            min_distance = abs(next_planet.x-planet.x)
                            min_planet = next_planet
                    self.make_link(min_planet,planet)

    def draw_links(self):
        for planet in self.planets:
            for link in planet.linked:
                for planet1 in self.planets:
                    if planet1.layer_x == link[0] and planet1.layer_y == link[1]:
                        pg.draw.line(self.image,WHITE,planet1.center,planet.center)

    def clicked(self,mouse_pos):
        mouse_pos = self.map_camera.apply_opp(mouse_pos)
        for planet in self.linked_planets:
            if planet.layer_y > self.current_planet.layer_y:
                #if a valid planet is clicked
                if abs(planet.center[0]-mouse_pos[0]) < 13 and abs(planet.center[1] - mouse_pos[1]) < 13:
                    self.current_planet = planet
                    self.image = pg.transform.scale(self.map_bg,(1920,WORLD_MAP_HEIGHT))
                    self.draw_links()
                    self.draw_planets()
                    self.image.blit(self.pointer_img,(self.current_planet.center[0]-45,self.current_planet.center[1]-53))

    def draw_text(self,surface,text,x,y,color,size):
        font = pg.font.Font(font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface,text_rect)

    def make_link(self,planet1,planet2):
        planet1.linked.append([planet2.layer_x,planet2.layer_y])
        planet2.linked.append([planet1.layer_x,planet1.layer_y])

    def update(self):
        self.map_camera.update(self.states)
        self.rect = self.map_camera.apply_rect(self.original_rect)
        self.linked_planets = []
        for planet in self.planets:
            if [planet.layer_x,planet.layer_y] in self.current_planet.linked:
                self.linked_planets.append(planet)

    def get_mouse(self,event):
        pass
