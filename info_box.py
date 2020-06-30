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
        self.ships = []
        self.length = 0 #length of ships
        for ship in ship_list:
            self.ships.append(ship)
            if ship.selected:
                self.length += 1
        print("test",len(self.ships))
        self.x = 0
        self.w = 600
        self.h = 450
        self.y = HEIGHT - self.h
        self.total_h = 80 * self.length
        self.rect = pg.Rect(self.x,self.y,self.w,self.h)
        self.image = pg.Surface((self.rect.w,self.rect.h))
        self.image.fill(DARKBLUE)
        self.button_image = self.game.buttons
        self.buttons = []
        #STATIC DRAWINGS (outline boxes, ship images) THIS WILL ONLY UPDATE WITH A NEW SHIP ADDITION
        for i in range(self.length):
            pg.draw.rect(self.image,BLUE3,pg.Rect(8,8+80*i,68,68),2) #draw ship outline box
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(10,10+80*i,65,65)) #draw ship outline background
            pg.draw.rect(self.image,BLUE3,pg.Rect(88,8+80*i,482,68),2) #draw info outline box
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(90,10+80*i,479,65)) #draw info outline backgroundd
            self.image.blit(pg.transform.rotate(self.ships[i].type,90),(10,10+80*i))
            self.game.draw_text(self.image,str("ID:"+str(self.ships[i].id)),295,15+80*i,WHITE,15)
            self.image.blit(self.button_image,(95,33+80*i))

            #new button stuff
            new_button = button('ATTACK',self.game,97+(BUTTON_W)*0,35+80*i+(BUTTON_H)*0,BUTTON_W,BUTTON_H)
            self.buttons.append(new_button)
            new_button = button('EVADE',self.game,97+(BUTTON_W)*1,35+80*i+(BUTTON_H)*0,BUTTON_W,BUTTON_H)
            self.buttons.append(new_button)
            new_button = button('IGNORE',self.game,97+(BUTTON_W)*0,35+80*i+(BUTTON_H)*1,BUTTON_W,BUTTON_H)
            self.buttons.append(new_button)
            new_button = button('NONE',self.game,97+(BUTTON_W)*1,35+80*i+(BUTTON_H)*1,BUTTON_W,BUTTON_H)
            self.buttons.append(new_button)

        if self.total_h > self.h:
            pg.draw.rect(self.image,DARKGREY,pg.Rect(580,10,10,int(self.h*self.h/self.total_h))) #draw scroll bar

    def update_text(self):
        for i in range(self.length-1):
            filler = ""
            while len(self.ships[i].task) + len(filler) < 10:
                filler += ' '
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(95,15+80*i,194,15)) #erase background of text
            self.game.draw_text(self.image,str("Task:"+str(self.ships[i].task)+filler+str("State:"+str(self.ships[i].state))),95,15+80*i,WHITE,15)

    def update(self):
        pass

#OLD
'''    def get_clicked(self,event,mouse_pos):
        output = []
        for button in self.buttons:
            if button.rect.move(0,HEIGHT - self.h).collidepoint(mouse_pos):
                output.append(button.clicked())
        return output

    def wipe(self):
        self.selected = 0
        self.total_h = 10
        self.ship_info_health = []
        self.ship_info_type = []
        self.ship_info_id = []
        self.buttons = []
        self.ship_info_task = []
        self.ship_info_state = []

        temp = pg.Surface((self.w-self.border,self.h-self.border))
        temp.fill(DARKGREY)
        self.image.blit(temp,(self.border,self.border))
        self.image.fill(BLUE3) #outline
        temp = pg.Surface((self.w-2*self.border,self.h-2*self.border))
        temp.fill(GREY1) #background
        self.image.blit(temp,(self.border,self.border))

    def add_ship(self,ship): #import info about ship
        self.ship_info_task.append(ship.task)
        self.ship_info_state.append(ship.state)
        self.ship_info_health.append(ship.health_bar.health)
        self.ship_info_type.append(ship.type)
        self.ship_info_id.append(ship.id)
        self.total_h += 80
        #old update
        self.selected = len(self.ship_info_type)
        #STATIC DRAWINGS (outline boxes, ship images) THIS WILL ONLY UPDATE WITH A NEW SHIP ADDITION
        i = len(self.ship_info_id)-1
        pg.draw.rect(self.image,BLUE3,pg.Rect(8,8+80*i,68,68),2) #draw ship outline box
        pg.draw.rect(self.image,DARKBLUE,pg.Rect(10,10+80*i,65,65)) #draw ship outline background
        pg.draw.rect(self.image,BLUE3,pg.Rect(88,8+80*i,482,68),2) #draw info outline box
        pg.draw.rect(self.image,DARKBLUE,pg.Rect(90,10+80*i,479,65)) #draw info outline backgroundd
        self.image.blit(pg.transform.rotate(self.ship_info_type[i],90),(10,10+80*i))
        #self.game.draw_text(self.image,str("Task:"+str(self.ship_info_task[i])),95,15+80*i,WHITE,15)
        self.game.draw_text(self.image,str("ID:"+str(self.ship_info_id[i])),295,15+80*i,WHITE,15)
        self.image.blit(self.button_image,(95,33+80*i))

        #new button stuff
        new_button = button('ATTACK',self.game,97+(BUTTON_W)*0,35+80*i+(BUTTON_H)*0,BUTTON_W,BUTTON_H,self.ship_info_id[i])
        self.buttons.append(new_button)
        new_button = button('EVADE',self.game,97+(BUTTON_W)*1,35+80*i+(BUTTON_H)*0,BUTTON_W,BUTTON_H,self.ship_info_id[i])
        self.buttons.append(new_button)
        new_button = button('IGNORE',self.game,97+(BUTTON_W)*0,35+80*i+(BUTTON_H)*1,BUTTON_W,BUTTON_H,self.ship_info_id[i])
        self.buttons.append(new_button)
        new_button = button('NONE',self.game,97+(BUTTON_W)*1,35+80*i+(BUTTON_H)*1,BUTTON_W,BUTTON_H,self.ship_info_id[i])
        self.buttons.append(new_button)

        if self.total_h > self.h:
            pg.draw.rect(self.image,DARKGREY,pg.Rect(580,10,10,int(self.h*self.h/self.total_h))) #draw scroll bar

    def set_command(self,id,state):
        i = self.ship_info_id.index(id)
        self.ship_info_task[i] = state

    def set_state(self,id,state):
        if id in self.ship_info_id:
            x = self.ship_info_id.index(id)
            self.ship_info_state[x] = state
            print('did some shit')

    def update(self): #add all the features to the base surface
        #FEATURES THAT NEED TO CHANGE (button)
        pass
        for button in self.buttons:
            self.image.blit(button.image,(button.x,button.y))
        for i in range(len(self.ship_info_id)):
            pg.draw.rect(self.image,DARKBLUE,pg.Rect(95,15+80*i,94,15)) #erase background of text
            self.game.draw_text(self.image,str("Task:"+str(self.ship_info_task[i])),95,15+80*i,WHITE,15)

            pg.draw.rect(self.image,DARKBLUE,pg.Rect(195,15+80*i,94,15)) #erase background of text
            self.game.draw_text(self.image,str("State:"+str(self.ship_info_state[i])),195,15+80*i,WHITE,15)'''
