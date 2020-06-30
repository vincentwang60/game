import pygame as pg
import os
import numpy as np
import math
from os import path
from settings import *
from sprites import *
from map import *
from camera import *

def move_formation(number,separation,destx,desty): #produces a list of destination coordinates based on separation
    targets = []
    square = math.ceil(number**0.5-0.01) #side length of square is square root of the number. ex. 4->2,10->4,15->4
    if square % 2 == 0: #even, then half separation for first round
        for x in range(square):
            for y in range(square):
                if len(targets)<number:
                    targets.append(tuple((destx - (square/2 - 0.5)*separation+x*separation,desty - (square/2-0.5)*separation+y*separation)))
                else:
                    return targets
    else: #odd, then normal center
        for x in range(square):
            for y in range(square):
                if len(targets)<number:
                    targets.append(tuple((destx - (square/2 - 0.5)*separation+x*separation,desty - (square/2-0.5)*separation+y*separation)))
                else:
                    return targets
    return targets

def attacking(attack_ships,target_ships):
    pass

class Game:
    def __init__(self):
        pg.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(400, 1)
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.mouse_pos = pg.mouse.get_pos()
        'game variables'
        self.selecting = False
        self.paused = False
        self.map_view = False
        self.draw_box = False
        self.commands = []

        'camera states'
        self.states = [False,False,False,False] #up, left, down, right

    def load_data(self):
        # directories
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,"sprites")
        self.image_surf = pg.image.load(path.join(img_folder,"f1_beam_ship.png")).convert_alpha()
        self.enemy_image_surf = pg.image.load(path.join(img_folder,"f2_beam_ship.png")).convert_alpha()
        self.planet1 = pg.image.load(path.join(img_folder,"planet1.png")).convert_alpha()
        self.planet2 = pg.image.load(path.join(img_folder,"planet2.png")).convert_alpha()
        self.planet3 = pg.image.load(path.join(img_folder,"planet3.png")).convert_alpha()
        self.planet4 = pg.image.load(path.join(img_folder,"planet4.png")).convert_alpha()
        self.planet5 = pg.image.load(path.join(img_folder,"planet5.png")).convert_alpha()
        self.planet6 = pg.image.load(path.join(img_folder,"planet6.png")).convert_alpha()
        self.star_surf = pg.image.load(path.join(img_folder,"star.png")).convert_alpha()
        self.buttons = pg.image.load(path.join(img_folder,"buttons.png")).convert_alpha()
        self.planets = [self.planet1,self.planet2,self.planet3,self.planet4,self.planet5,self.planet6]

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.ui = pg.sprite.Group()
        self.ally_ships = pg.sprite.Group()
        self.enemy_ships = pg.sprite.Group()
        self.map_group = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.health_bar = pg.sprite.Group()

        for i in range(20):
            self.s = ship(self,200+20*i,200,i+200)
        enemy_ship(self,1050,150)
        self.box = select_box(self)
        self.map = g_map(self)
        self.bg = bg(self)
        self.camera = camera()
        self.info_box = info_box(self)
        for i in range(int(STAR_DENSITY * MAP_SIZE[0]*MAP_SIZE[1])):
            star(self)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()

    def update(self):
        # update portion of the game loop
        self.mouse_pos = pg.mouse.get_pos()
        if self.selecting:
            self.selected_area = self.camera.apply_rect(self.box.make_rect())
            for ship in self.ally_ships:
                ship.set_selected()
        else:
            self.selected_area = pg.Rect(-2,-2,-1,-1)
        self.all_sprites.update()
        self.camera.update(self.states)

        #issue commands & states
        for ship in self.ally_ships:
            if ship.selected:
                self.info_box.set_state(ship.id,ship.state)
        for command in self.commands:
            for ship in self.ally_ships:
                #issue commands
                if ship.id == command[0]:
                    ship.task = command[1]
                    self.info_box.set_command(ship.id,ship.task)

    def draw(self):
        if self.map_view:
            self.screen.fill(BLACK)
        else:
            self.screen.fill(PURPLE)
        for i in self.stars:
            self.screen.blit(i.image,(self.camera.apply(i).x,self.camera.apply(i).y))
        for i in self.background:
            self.screen.blit(i.image,(self.camera.apply(i).x,self.camera.apply(i).y))
        #self.background.draw(self.screen)
        if not self.map_view:
            for i in self.ally_ships:
                self.screen.blit(i.image,(self.camera.apply(i).x,self.camera.apply(i).y))
            for ship in self.ally_ships:
                if ship.selected:
                    pg.draw.line(self.screen,DARKGREY,self.camera.apply_opp(ship.make_line()[0]),self.camera.apply_opp(ship.make_line()[1]))
            for i in self.enemy_ships:
                self.screen.blit(i.image,(self.camera.apply(i).x,self.camera.apply(i).y))
        else:
            self.map_group.draw(self.screen)
        for i in self.health_bar:
            self.screen.blit(i.image,(self.camera.apply(i).x,self.camera.apply(i).y))
        self.ui.draw(self.screen)
        if self.draw_box:
            self.screen.blit(self.info_box.image,(self.info_box.x,self.info_box.y))
        self.draw_text(self.screen,str(self.camera.state),200,100,WHITE,30) #TEXT TEXT TEXT
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused
                if event.key == pg.K_m:
                    self.map_view = not self.map_view
                if event.key == pg.K_a:
                    self.states[1] = True
                if event.key == pg.K_w:
                    self.states[0] = True
                if event.key == pg.K_s:
                    self.states[2] = True
                if event.key == pg.K_d:
                    self.states[3] = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    self.states[1] = False
                if event.key == pg.K_w:
                    self.states[0] = False
                if event.key == pg.K_s:
                    self.states[2] = False
                if event.key == pg.K_d:
                    self.states[3] = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.commands = self.info_box.get_clicked(event,(self.mouse_pos[0],self.mouse_pos[1]))
                    if self.draw_box and (self.mouse_pos[0]<600 and self.mouse_pos[1]>HEIGHT-450):
                        pass
                    else: #create select box
                        for sprite in self.ally_ships:
                            sprite.selected = False
                        self.selecting = True
                        self.box.set_start(self.mouse_pos[0],self.mouse_pos[1])
                if event.button == 3: #move command
                    gen = (x for x in self.ally_ships if x.selected)
                    selected = []
                    number_selected = 0
                    for x in gen:
                        number_selected+=1
                        selected.append(x)
                    targets = move_formation(number_selected,30,self.mouse_pos[0],self.mouse_pos[1])
                    counter = 0
                    for sprite in selected:
                        target = targets[counter]
                        target = self.camera.apply_point(targets[counter])
                        sprite.set_dest(target)
                        counter+=1
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.selecting:
                        self.selecting = False
                        #once the box is finalized, make the info_box
                        self.draw_box = True
                        self.info_box.wipe()
                        for ship in self.ally_ships:
                            self.info_box.add_ship(ship)
                        self.box.set_start(2000,2000)

    def start_screen(self):
        pass

    def end_screen(self):
        pass

    def draw_text(self,surface,text,x,y,color,size):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface,text_rect)

# create the game object
g = Game()
g.start_screen()
while True:
    g.new()
    g.run()
    g.end_screen()
