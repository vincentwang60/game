import pygame as pg
import numpy as np
import random
from settings import *

class select_box(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = [game.ui,game.all_sprites]
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.mx = -1
        self.my = -1
        self.startx = -2
        self.starty = -2
        self.image = pg.Surface((1,1))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def set_start(self,x,y):
        self.startx=  x
        self.starty = y
    def update(self):
        if self.game.selecting:
            self.mx = self.game.mouse_pos[0]
            self.my = self.game.mouse_pos[1]
            self.image = pg.Surface((abs(self.mx-self.startx), abs(self.my - self.starty)))
            self.rect = self.make_rect()
            self.image.set_colorkey(BLACK)
            self.image.fill((37,84,199))
            self.image.fill(BLACK,pg.Rect(2,2,abs(self.mx-self.startx)-4,abs(self.my-self.starty)-4))
        else:
            self.mx = -1
            self.my = -1
            self.startx = -2
            self.starty = -2
            self.image = pg.Surface((abs(self.mx-self.startx), abs(self.my - self.starty)))
            self.rect = self.make_rect()

    def make_rect(self):
        self.mx = self.game.mouse_pos[0]
        self.my = self.game.mouse_pos[1]
        left = 0
        top = 0
        width = 1
        height = 1
        if self.mx > self.startx:
            left = self.startx
        else:
            left = self.mx
        if self.my > self.starty:
            top = self.starty
        else:
            top = self.my
        return pg.Rect(left,top,abs(self.mx-self.startx),abs(self.my-self.starty))

    def get_mouse(self,event):
        pass

class star(pg.sprite.Sprite): #100 for 1920/1080
    def __init__(self,game):
        self.groups = [game.stars,game.all_sprites]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.w = 3+random.randrange(3)
        self.scale = 0.1 + random.uniform(0,0.3)
        self.image = self.game.star_surf.copy()
        self.image = pg.transform.scale(self.game.star_surf,(int(16*self.scale),int(16*self.scale)))
        rand = random.randrange(3)
        r = 0
        b= 0
        if rand == 0:
            r = 50+random.randrange(100)
            self.image.fill((r,0,b,255),special_flags=pg.BLEND_ADD)
        elif rand == 1:
            b = 50 + random.randrange(100)
            self.image.fill((r,0,b,255),special_flags=pg.BLEND_ADD)
        self.rect = self.image.get_rect()
        self.rect.x = -(MAP_SIZE[0]-WIDTH)/2+random.randrange(MAP_SIZE[0])
        self.rect.y = -(MAP_SIZE[1]-HEIGHT)/2+random.randrange(MAP_SIZE[1])
    def update(self):
        pass

class bg(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = [game.background,game.all_sprites]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.planets[random.randrange(6)]
        self.image.fill((random.randrange(50), random.randrange(50), random.randrange(50), 100), special_flags=pg.BLEND_SUB)
        self.image = pg.transform.rotate(self.image,random.randrange(360))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
    def update(self):
        pass

class health_bar(pg.sprite.Sprite):
    def __init__(self,game,x,y,bars):
        self.groups = [game.health_bar,game.all_sprites]
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((67,5*bars+5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.bars = bars
        self.y = y
        self.health_rects = []
        for i in range(bars):
            self.health_rects.append(pg.Rect(2,2+5*i,60,4))
        self.max_health = [100,100,100]
        self.health = [100,100,100]

    def __del__(self):
        self.image = pg.Surface((1,1))
        self.image.fill(BLACK)

    def update(self):
        #draw grey background of bar
        temp = pg.Surface((63,5*self.bars+1))
        temp.fill(LIGHTGREY)
        self.image.blit(temp,(2,2))
        #makes sure health isn't negative
        for health in self.health:
            if health < 0:
                health = 0

        #draw health bars
        for i in range(self.bars):
            self.health_rects[i].w = 63*self.health[i]/self.max_health[i]
        temp = pg.Surface((self.health_rects[0].w,self.health_rects[0].h))
        temp.fill((65,105,225))
        self.image.blit(temp,(2,2))
        if self.bars == 3:
            temp = pg.Surface((self.health_rects[2].w,self.health_rects[2].h))
            temp.fill(RED)
            self.image.blit(temp,(2,2+6))

            temp = pg.Surface((self.health_rects[1].w,self.health_rects[1].h))
            temp.fill((255,215,0))
            self.image.blit(temp,(2,2+6*2))
        else:
            temp = pg.Surface((self.health_rects[1].w,self.health_rects[1].h))
            temp.fill((255,215,0))
            self.image.blit(temp,(2,2+6))


        #draw grid of bar
        for x in range(1,11):
            temp = pg.Surface((1,5*self.bars+1))
            temp.fill(BLACK)
            self.image.blit(temp,(x*6,2))

        for x in range(1,self.bars):
            temp = pg.Surface((67,2))
            temp.fill(BLACK)
            self.image.blit(temp,(0,6*x))

        self.rect.x = self.x - 32
        self.rect.y = self.y - 20

class ship(pg.sprite.Sprite):
    def __init__(self, game, x, y,id,img_string,fleet = None,leader = False):
        '''ship variables'''
        self.selected = False
        self.in_range = False
        self.rclick_moving = False
        self.killed = False

        self.angle = 0
        self.x = x
        self.y = y
        self.vel = 300
        self.target_angle = 1
        self.rot_speed = 10
        self.destx = x
        self.desty= y
        self.id = id
        self.reload_delay = 100
        self.reload_tick = 0
        self.range = BEAM_RANGE
        self.dmg = 10
        self.dying_tick = 0
        self.fleet = fleet #for enemy ships
        self.leader = leader #for enemy ships
        self.fired = False #keeps track of if its fired for the first time
        self.target_ship_id = 0
        self.img_string = img_string

        self.task = 'IGNORE' #what its goal is
        self.state = 'Idle' #what its currently doing
        if img_string == 'f1_beam': #self. img = original image
            self.scale = 0.5
            self.img = game.f1_beam
            self.groups = [game.ally_ships,game.all_sprites]
        elif img_string == 'f2_beam': #enemies
            self.dmg = 1
            self.scale = 1
            self.img = game.f2_beam
            self.groups = [game.enemy_ships,game.all_sprites]
        elif img_string == 'f1_capital':
            self.scale = 1
            self.img = game.f1_capital
            self.groups = [game.ally_ships,game.all_sprites]
        self.attack_target_pos = [0,0]
        self.alive = True
        '''end of ship variables'''

        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(self.img,self.angle)
        self.rect = self.image.get_rect()
        self.original_width = self.rect.width
        self.original_height = self.rect.height
        self.image.set_colorkey(WHITE)

        self.health_bar = health_bar(self.game,self.x,self.y,2)

    def damage(self,dmg,dmg_type):
        if not self.game.paused:
            if self.health_bar.health[0]>0: #shields
                self.health_bar.health[0] -= 2*dmg
            elif self.health_bar.health[1]>0: #hull
                self.health_bar.health[1] -= dmg
                self.health_bar.health[2] -= dmg
            elif self.health_bar.health[2]>0: #crew
                self.health_bar.health[2] -= dmg
            if self.health_bar.health[1] <= 0:
                self.kill()


    def fire(self):
        if self.reload_tick == self.reload_delay: #fire if not reloading once it reaches top
            self.fired = True
            if not self.game.paused:
                self.reload_tick = 0
            #if firing, return damage and target
            return [self.dmg,self.attack_target]
        elif self.reload_tick < BEAM_DURATION and self.fired:
            if not self.game.paused:
                self.reload_tick += 1
            return [0,self.attack_target]
        else: #if its not drawing its beam, resets fired to false
            self.fired = False
            if not self.game.paused:
                self.reload_tick += 1
            return False

    def resize(self):
        self.image = pg.transform.scale(self.img,(int(self.original_width*self.scale),int(self.original_height*self.scale)))

    def get_target_angle(self):
        return -(np.arctan2(self.desty-self.y, self.destx-self.x) * 180 / np.pi)

    def move(self, dx=0, dy=0):
        if abs(self.x-self.destx) > 10 or abs(self.y-self.desty)>10: #if unsatisfied with position
            while self.target_angle >= 180:
                self.target_angle -= 360
            while self.target_angle <= -180:
                self.target_angle += 360
            self.x += self.vel*self.game.dt*np.cos(np.pi*self.angle/180)
            self.y += -self.vel*self.game.dt*np.sin(np.pi*self.angle/180)
            self.target_angle = self.get_target_angle()
        elif self.task != 'ATTACK' or self.state == 'Moving to position':
            self.state = 'Idle'

        if abs(self.target_angle-self.angle)>5: #unsatisfied with angle
            while self.angle >= 180:
                self.angle -= 360
            while self.angle <= -180:
                self.angle += 360
            if self.target_angle < 0 and self.angle <=0:
                if self.target_angle > self.angle:
                    self.angle += self.rot_speed
                else:
                    self.angle -= self.rot_speed
            elif self.target_angle < 0:
                if abs(self.target_angle) + abs(self.angle) > 180:
                    self.angle += self.rot_speed
                else:
                    self.angle -= self.rot_speed
            elif self.angle < 0:
                if abs(self.angle)+abs(self.target_angle) > 180:
                    self.angle -= self.rot_speed
                else:
                    self.angle += self.rot_speed
            elif self.angle > self.target_angle:
                self.angle -= self.rot_speed
            else:
                self.angle += self.rot_speed
        else: #if close enough, make angle the target
            self.angle = self.target_angle

    def get_outline(self,color=(0,0,0)):
        rect = self.image.get_rect()
        mask = pg.mask.from_surface(self.image)
        outline = mask.outline()
        outline_image = pg.Surface(rect.size).convert_alpha()
        outline_image.fill((0,0,0,0))
        for point in outline:
            outline_image.set_at(point,color)

        merged = self.image.copy()
        merged.blit(outline_image, (0, 0))
        self.image = merged

    def make_line(self,color=(255,0,0)):
        if self.target_ship_id != 0 and self.state != "Moving to position": #if there is a forced target and no r-click order
            for ship in self.game.enemy_ships:
                if ship.id == self.target_ship_id:
                    return [(self.x,self.y),(ship.x,ship.y)] #draws line to enemy ship\
        return [(self.x,self.y),(self.destx,self.desty)]

    def set_target_angle(self,target):
        self.target_angle = -(np.arctan2(target[1]-self.y, target[0]-self.x) * 180 / np.pi)

    def set_dest(self,dest):
        self.destx = dest[0]
        self.desty= dest[1]

    def set_selected(self):
        if self.game.selected_area.colliderect(pg.Rect((self.x-20*self.scale,self.y-20*self.scale),(40*self.scale,40*self.scale))) and self.game.ally_ships in self.groups:
            self.selected = True
        else:
            self.selected = False
        return self.selected

    def kill(self):
        self.alive = 'dying'
        self.rect = pg.Rect(0,0,100,100)
        self.image = self.game.explosion[0]

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.image.get_rect().center
        self.rect.centerx = self.x
        self.rect.centery = self.y
        #if its dying
        if self.alive == 'dying':
            if self.dying_tick < 23:
                self.dying_tick += 1
                self.image = self.game.explosion[int(self.dying_tick)]
            else:
                self.alive = 'dead'
                self.dying_tick = 0
        else:
            if not self.game.paused:
                self.move()
            self.resize()
            self.image = pg.transform.rotate(self.image,self.angle)

            if self.selected:
                self.get_outline(YELLOW)
            self.health_bar.x = self.rect.midtop[0]
            self.health_bar.y = self.rect.midtop[1]
