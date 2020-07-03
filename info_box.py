import pygame as pg
import numpy as np
import random
from settings import *

class button(pg.sprite.Sprite):
    def __init__(self,type,game,x,y,w,h,owner = None):
        self.groups = [game.all_sprites]
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.type = type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.owner_id = owner
        self.image = pg.Surface((w,h))
        self.rect = pg.Rect(self.x,self.y,w,h)

    def clicked(self):
        return (self.owner_id,self.type)

class info_box(pg.sprite.Sprite):
    def __init__(self,game,ship_list):
        self.groups = [game.all_sprites]
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game

        'VARIABLES'
        self.ships = []
        self.x = 0
        self.w = 600
        self.h = 498
        self.y = HEIGHT - self.h
        self.rect = pg.Rect(self.x,self.y,self.w,self.h)
        self.image = pg.Surface((self.rect.w,self.rect.h))
        self.image.fill((1,1,1))
        self.image.set_colorkey((1,1,1))
        pg.draw.rect(self.image,DARKGREY,pg.Rect(self.x,48,self.w,self.h),2) #draw ship outline box
        pg.draw.rect(self.image,GREY1,pg.Rect(2,50,self.w-3,self.h-4)) #draw ship outline background
        self.button_image = self.game.buttons
        self.top_button_image = self.game.top_buttons
        self.buttons = []
        self.top_buttons = []
        self.icon = []
        'END OF VARIABLEs'

        for ship in ship_list:
            if ship.selected:
                self.ships.append(ship)

        self.f1_beam_img = self.game.f1_beam.copy()
        self.f1_capital_img = self.game.f1_capital.copy()
        self.f1_beam_img = pg.transform.scale(self.f1_beam_img,(68,68))
        self.f1_capital_img = pg.transform.scale(self.f1_capital_img,(68,34))
        self.total_h = 80 * len(self.ships)
        #STATIC DRAWINGS (outline boxes, ship images, buttons) THIS WILL ONLY UPDATE WITH A NEW SHIP ADDITION
        self.image.blit(self.top_button_image,(0,0))
        for i in range(len(self.ships)):
            pg.draw.rect(self.image,BLUE3,pg.Rect(8,56+80*i,68,68),2) #draw ship outline box
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(10,58+80*i,65,65)) #draw ship outline background
            pg.draw.rect(self.image,BLUE3,pg.Rect(88,56+80*i,482,68),2) #draw info outline box
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(90,58+80*i,479,65)) #draw info outline backgroundd
            if self.ships[i].img_string == 'f1_beam':
                self.image.blit(pg.transform.rotate(self.f1_beam_img,90),(10,58+80*i))
            else:
                self.image.blit(pg.transform.rotate(self.f1_capital_img,90),(10,58+80*i))
            self.game.draw_text(self.image,str("ID:"+str(self.ships[i].id)),395,63+80*i,WHITE,15)
            self.image.blit(self.button_image,(95,81+80*i))

            #new button stuff
            new_button = button('ATTACK',self.game,97+(BUTTON_W)*0,83+80*i+(BUTTON_H)*0,BUTTON_W,BUTTON_H,self.ships[i].id)
            self.buttons.append(new_button)
            new_button = button('EVADE',self.game,97+(BUTTON_W)*1,83+80*i+(BUTTON_H)*0,BUTTON_W,BUTTON_H,self.ships[i].id)
            self.buttons.append(new_button)
            new_button = button('IGNORE',self.game,97+(BUTTON_W)*0,83+80*i+(BUTTON_H)*1,BUTTON_W,BUTTON_H,self.ships[i].id)
            self.buttons.append(new_button)
            new_button = button('RETREAT',self.game,97+(BUTTON_W)*1,83+80*i+(BUTTON_H)*1,BUTTON_W,BUTTON_H,self.ships[i].id)
            self.buttons.append(new_button)

        new_button = button('ALL ATTACK',self.game,4,4,148,40)
        self.top_buttons.append(new_button)
        new_button = button('ALL IGNORE',self.game,152,4,148,40)
        self.top_buttons.append(new_button)
        new_button = button('ALL EVADE',self.game,300,4,148,40)
        self.top_buttons.append(new_button)
        new_button = button('ALL RETREAT',self.game,448,4,148,40)
        self.top_buttons.append(new_button)

        if self.total_h > self.h:
            pg.draw.rect(self.image,DARKGREY,pg.Rect(580,58,10,int(self.h*self.h/self.total_h))) #draw scroll bar

    def clicked(self,mouse_pos): #activates when left clicked inside the info box
        for button in self.buttons:
            #if button is clicked
            if button.rect.move(0,HEIGHT - self.h).collidepoint(mouse_pos):
                #searches list of ships for id, and sets that ships task to the button effect
                button_effect = button.clicked()
                for ship in self.ships:
                    if ship.id == button_effect[0]:
                        ship.task = button_effect[1]

        for button in self.top_buttons:
            #if button is clicked
            if button.rect.move(0,HEIGHT - self.h).collidepoint(mouse_pos):
                if button.type[:3] == 'ALL':
                    for ship in self.ships:
                        if ship.selected:
                            ship.task = button.type[4:]
                #searches list of ships for id, and sets that ships task to the button effect
                button_effect = button.clicked()
                for ship in self.ships:
                    if ship.id == button_effect[0]:
                        ship.task = button_effect[1]

    def update_text(self):
        for i in range(len(self.ships)):
            filler = ""
            while len(self.ships[i].task) + len(filler) < 10:
                filler += ' '
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(95,63+80*i,294,15)) #erase background of text
            self.game.draw_text(self.image,str("Task:"+str(self.ships[i].task)+filler+str("State:"+str(self.ships[i].state))),95,63+80*i,WHITE,15)

    def update(self):
        pass
