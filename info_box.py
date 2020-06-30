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
        self.owner_id = owner
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pg.Surface((w,h))
        self.image.set_colorkey(BLACK)
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
        self.length = 0 #length of ships
        self.x = 0
        self.w = 600
        self.h = 450
        self.y = HEIGHT - self.h
        self.total_h = 80 * self.length
        self.rect = pg.Rect(self.x,self.y,self.w,self.h)
        self.image = pg.Surface((self.rect.w,self.rect.h))
        pg.draw.rect(self.image,DARKGREY,pg.Rect(self.x,0,self.w,self.h),2) #draw ship outline box
        pg.draw.rect(self.image,GREY1,pg.Rect(2,2,self.w-3,self.h-4)) #draw ship outline background
        self.button_image = self.game.buttons
        self.buttons = []
        'END OF VARIABLEs'

        for ship in ship_list:
            self.ships.append(ship)
            if ship.selected:
                self.length += 1

        #STATIC DRAWINGS (outline boxes, ship images, buttons) THIS WILL ONLY UPDATE WITH A NEW SHIP ADDITION
        for i in range(self.length):
            pg.draw.rect(self.image,BLUE3,pg.Rect(8,8+80*i,68,68),2) #draw ship outline box
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(10,10+80*i,65,65)) #draw ship outline background
            pg.draw.rect(self.image,BLUE3,pg.Rect(88,8+80*i,482,68),2) #draw info outline box
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(90,10+80*i,479,65)) #draw info outline backgroundd
            self.image.blit(pg.transform.rotate(self.ships[i].type,90),(10,10+80*i))
            self.game.draw_text(self.image,str("ID:"+str(self.ships[i].id)),295,15+80*i,WHITE,15)
            self.image.blit(self.button_image,(95,33+80*i))

            #new button stuff
            new_button = button('ATTACK',self.game,97+(BUTTON_W)*0,35+80*i+(BUTTON_H)*0,BUTTON_W,BUTTON_H,self.ships[i].id)
            self.buttons.append(new_button)
            new_button = button('EVADE',self.game,97+(BUTTON_W)*1,35+80*i+(BUTTON_H)*0,BUTTON_W,BUTTON_H,self.ships[i].id)
            self.buttons.append(new_button)
            new_button = button('IGNORE',self.game,97+(BUTTON_W)*0,35+80*i+(BUTTON_H)*1,BUTTON_W,BUTTON_H,self.ships[i].id)
            self.buttons.append(new_button)
            new_button = button('RETREAT',self.game,97+(BUTTON_W)*1,35+80*i+(BUTTON_H)*1,BUTTON_W,BUTTON_H,self.ships[i].id)
            self.buttons.append(new_button)

        if self.total_h > self.h:
            pg.draw.rect(self.image,DARKGREY,pg.Rect(580,10,10,int(self.h*self.h/self.total_h))) #draw scroll bar

    def clicked(self,mouse_pos): #activates when left clicked inside the info box
        for button in self.buttons:
            #if button is clicked
            if button.rect.move(0,HEIGHT - self.h).collidepoint(mouse_pos):
                #searches list of ships for id, and sets that ships task to the button effect
                button_effect = button.clicked()
                for ship in self.ships:
                    print(button_effect)
                    if ship.id == button_effect[0]:
                        print("before: ",ship.task)
                        ship.task = button_effect[1]
                        print("after: ",ship.task)

    def update_text(self):
        for i in range(self.length-1):
            filler = ""
            while len(self.ships[i].task) + len(filler) < 10:
                filler += ' '
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(95,15+80*i,194,15)) #erase background of text
            self.game.draw_text(self.image,str("Task:"+str(self.ships[i].task)+filler+str("State:"+str(self.ships[i].state))),95,15+80*i,WHITE,15)

    def update(self):
        pass
