import pygame as pg
import os
import numpy as np
from os import path
from settings import *
from sprites import *
from map import *
from camera import *
from info_box import *
from ship_mngr import *
from spritesheet import *

class Game:
    def __init__(self):
        'DONT TOUCH'
        pg.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(400, 1)
        self.load_data()
        self.mouse_pos = pg.mouse.get_pos()

        'game variables'
        self.selecting = False
        self.paused = False
        self.map_view = False
        self.draw_box = False
        self.commands = []
        self.delayed_timer = 0
        self.delayed_timer_max = 20
        self.enemy_exists = False
        self.map_scroll_vel = 0
        self.states = [False,False,False,False] #contains game variables

    def load_data(self): #loads new pngs
        # directories
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,"sprites")

        self.f1_beam = pg.image.load(path.join(img_folder,"f1_beam_ship.png")).convert_alpha()
        self.f2_beam = pg.image.load(path.join(img_folder,"f2_beam_ship.png")).convert_alpha()
        self.planet1 = pg.image.load(path.join(img_folder,"planet1.png")).convert_alpha()
        self.planet2 = pg.image.load(path.join(img_folder,"planet2.png")).convert_alpha()
        self.planet3 = pg.image.load(path.join(img_folder,"planet3.png")).convert_alpha()
        self.planet4 = pg.image.load(path.join(img_folder,"planet4.png")).convert_alpha()
        self.planet5 = pg.image.load(path.join(img_folder,"planet5.png")).convert_alpha()
        self.planet6 = pg.image.load(path.join(img_folder,"planet6.png")).convert_alpha()
        self.star_surf = pg.image.load(path.join(img_folder,"star.png")).convert_alpha()
        self.buttons = pg.image.load(path.join(img_folder,"buttons.png")).convert_alpha()
        self.f1_capital = pg.image.load(path.join(img_folder,"f1_capital.png")).convert_alpha()
        self.top_buttons = pg.image.load(path.join(img_folder,"top_buttons.png")).convert_alpha()
        self.pointer = pg.image.load(path.join(img_folder,"point.png")).convert_alpha()
        self.map_bg = pg.image.load(path.join(img_folder,"map.png")).convert_alpha()
        self.paused_img = pg.image.load(path.join(img_folder,'paused.png')).convert_alpha()
        self.planets = [self.planet1,self.planet2,self.planet3,self.planet4,self.planet5,self.planet6]

        ss = spritesheet(path.join(img_folder,"explosion.png"))
        self.explosion = ss.load_strip(pg.Rect(0,0,100,100),24,BLUE)

    def new(self):
        #test
        self.all_sprites = pg.sprite.Group()
        self.ui = pg.sprite.Group()
        self.ally_ships = pg.sprite.Group()
        self.enemy_ships = pg.sprite.Group()
        self.map_group = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.health_bar = pg.sprite.Group()

        'SPAWN STARTING SHIPS'
        for i in range(5):
            self.s = ship(self,200+20*i,200,i+200,'f1_beam')
        self.s = ship(self,500,200,200,'f1_capital')
        self.enemy_fleets = []

        self.box = select_box(self)
        self.map = g_map(self)
        self.bg = bg(self)
        self.camera = camera()
        self.info_box = info_box(self,self.ally_ships)
        self.ship_mngr = ship_mngr(self)
        self.ship_mngr.add_fleet(self.ally_ships,True)
        self.ship_mngr.add_fleet(self.enemy_ships,False)

        for i in range(int(STAR_DENSITY * MAP_SIZE[0]*MAP_SIZE[1])):
            star(self) #does all startup activity, creates groups, stars, background

    def warp(self): #if in the map view, clicks next planet
        self.bg.change(self) #changes background
        'SPAWN NEW ENEMIES'
        ship(self,200,600,200,'f2_beam',1,True) #fleet leader
        for i in range(1,5): #fleet others
            self.s = ship(self,200+20*i,600,i+200,'f2_beam',1,False)
        for ally_ship in self.ally_ships:
            if ally_ship.alive:
                ally_ship.y = 1900
                ally_ship.health_bar.health[0] = ally_ship.health_bar.max_health[0]
                ally_ship.destx = ally_ship.x
                ally_ship.desty = ally_ship.y
        self.enemy_fleets = [1] #list of enemy groups (fleets)

    def run(self): #main game loop, dont touchmm
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit() #ends game, dont touch

    def kill_ships(self,group):
        for ship in group:
            if ship.alive == 'dying' and not ship.killed:
                ship.killed = True
                self.all_sprites.remove(ship.health_bar)
                self.health_bar.remove(ship.health_bar)
                #del ship.health_bar
            if ship.alive == 'dead':
                self.all_sprites.remove(ship)
                group.remove(ship)
                del ship
                self.ship_mngr.refresh_ships(self.ally_ships,self.enemy_ships)
                self.info_box = info_box(self,self.ally_ships)

    def update(self):
        # update portion of the game loop
        self.mouse_pos = pg.mouse.get_pos()
        #smooth scrolling
        if self.map.map_camera.y + self.map_scroll_vel>= 0 and self.map.map_camera.y + self.map_scroll_vel< 2332:
            self.map.map_camera.y += self.map_scroll_vel
        if self.map_scroll_vel > 0:
            self.map_scroll_vel -= 10
        if self.map_scroll_vel < 0:
            self.map_scroll_vel += 10

        if self.selecting:
            self.selected_area = self.camera.apply_rect(self.box.make_rect())
            for ship in self.ally_ships:
                ship.set_selected()
        else:
            self.selected_area = pg.Rect(-2,-2,-1,-1)
        self.all_sprites.update()
        self.camera.update(self.states)
        #update text after a delay
        if self.delayed_timer < self.delayed_timer_max:
            self.delayed_timer += 1
        else:
            self.info_box.update_text()
            self.delayed_timer = 0

        #KILL DEAD SHIPS
        self.kill_ships(self.ally_ships)
        self.kill_ships(self.enemy_ships)

        self.ship_mngr.refresh_ships(self.ally_ships,self.enemy_ships)
        self.ship_mngr.update()

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
        'DRAWS THE THINGS UNDER MAP'
        if not self.map_view:
            for i in self.ally_ships:
                self.screen.blit(i.image,(self.camera.apply(i).x,self.camera.apply(i).y))
            for ship in self.ally_ships:
                if ship.selected:
                    pg.draw.line(self.screen,DARKGREY,self.camera.apply_opp(ship.make_line()[0]),self.camera.apply_opp(ship.make_line()[1]))
            for i in self.enemy_ships:
                self.screen.blit(i.image,(self.camera.apply(i).x,self.camera.apply(i).y))
            for i in self.health_bar:
                self.screen.blit(i.image,(self.camera.apply(i).x,self.camera.apply(i).y))

            'DRAW LASERS AND FIRE'
            for ship in self.ally_ships:
                if ship.task == 'ATTACK' and ship.in_range and ship.state != 'Moving to position' and self.enemy_exists:
                    info = ship.fire()
                    if info !=False: #if it's firing
                        for enemy_ship in self.enemy_ships:
                            if enemy_ship.id == info[1]:
                                enemy_ship.damage(info[0],'beam')
                        pg.draw.line(self.screen,RED,self.camera.apply_opp((ship.x,ship.y)),self.camera.apply_opp((ship.attack_target_pos[0],ship.attack_target_pos[1])),4)
            'DRAW ENEMY LASER AND FIRE'
            for ship in self.enemy_ships:
                if ship.in_range:
                    info = ship.fire()
                    if info !=False: #if it's firing
                        for enemy_ship in self.ally_ships:
                            if enemy_ship.id == info[1]:
                                enemy_ship.damage(info[0],'beam')
                        pg.draw.line(self.screen,BLUE,self.camera.apply_opp((ship.x,ship.y)),self.camera.apply_opp((ship.attack_target_pos[0],ship.attack_target_pos[1])),4)

            #DRAWS UI
            self.ui.draw(self.screen)
            if self.draw_box:
                self.screen.blit(self.info_box.image,(self.info_box.x,self.info_box.y))
            if self.paused:
                self.screen.blit(self.paused_img,(755,0))
        else:
            'DRAWS STUFF ON THE MAP'
            self.map_group.draw(self.screen)
            #self.draw_text(self.screen,str(self.map.map_camera.y),200,100,WHITE,30) #TEXT TEXT TEXT
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
                if event.key == pg.K_l:
                    self.ship_mngr.print()
                if event.key == pg.K_m:
                    self.map_view = not self.map_view
                    self.paused = True
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
                'LEFT CLICK'
                if event.button == 1:
                    if self.map_view and not self.enemy_exists:
                        self.map.clicked(self.mouse_pos)
                        self.warp()
                    else:
                        #if theres a box and we click inside it
                        if self.draw_box and (self.mouse_pos[0]<600 and self.mouse_pos[1]>HEIGHT-508):
                            self.info_box.clicked(self.mouse_pos) #tell info box where we clicked
                        else: #if we click in a valid spot in the background
                            self.draw_box = False
                            for sprite in self.ally_ships:
                                sprite.selected = False
                            self.selecting = True
                            self.box.set_start(self.mouse_pos[0],self.mouse_pos[1])
                        self.ship_mngr.l_click(self.mouse_pos)
                'RIGHT CLICK'
                if event.button == 3: #move command
                    self.ship_mngr.r_click(self.mouse_pos)
                'map scrolling'
                if self.map_view:
                    if event.button == 4:
                        self.map_scroll_vel = -3*SCROLL_SPEED
                    if event.button == 5:
                        self.map_scroll_vel = 3*SCROLL_SPEED
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.selecting:
                        self.selecting = False
                        #once the box is finalized, make the info_box
                        self.info_box = info_box(self,self.ally_ships)
                        if any(ship.selected for ship in self.ally_ships):
                            self.draw_box = True
                        for ship in self.ally_ships:
                            pass#self.info_box.add_ship(ship)
                        self.box.set_start(2000,2000)

    def start_screen(self):
        pass

    def end_screen(self):
        pass

    def draw_text(self,surface,text,x,y,color,size):
        font = pg.font.Font(font_name,size)
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
