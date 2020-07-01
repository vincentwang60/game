import pygame as pg
import random
import numpy as np
from settings import *
import math

class ship_mngr(): #issues move commands to ships
    def __init__(self,game):
        self.game = game
        'VARIABLES'
        self.ally_ships = []
        self.enemy_ships = []
        self.attacking = []
        self.evading = []
        self.ignoring = []
        self.retreating = []
        self.separation = 450
        self.close_separation = 300

    def l_click(self,mouse_pos):
        self.make_lists()


    def make_lists(self):
        self.attacking = (x for x in self.ally_ships if (x.selected and x.task == 'ATTACK')) #list of ships that are selected & attacking
        self.evading = (x for x in self.ally_ships if (x.selected and x.task == 'EVADE')) #list of ships that are selected & evading
        self.ignoring = (x for x in self.ally_ships if (x.selected and x.task == 'IGNORE')) #list of ships that are selected & ignoring
        self.retreating = (x for x in self.ally_ships if (x.selected and x.task == 'RETREAT')) #list of ships that are selected & retreating
        self.selected = (x for x in self.ally_ships if (x.selected)) #list of selected ships

    def r_click(self,mouse_pos): #handles if user right clicks
        selected_list = []
        for ship in self.selected:
            selected_list.append(ship)
        self.make_lists()
        targets = self.move_formation(len(selected_list),30,mouse_pos[0],mouse_pos[1]) #make list of target dests
        for i in range(len(selected_list)):
            target = self.game.camera.apply_point(targets[i])
            selected_list[i].set_dest(target)
            selected_list[i].state = 'Moving to position'

    def find_closest(self,start_ship):
        closest = 9999
        output = None
        for ship in self.enemy_ships:
            dist = self.distance((start_ship.x,start_ship.y),(ship.x,ship.y))
            if dist < closest:
                closest = dist
                output = ship
        return output

    def distance(self,point1,point2):
        return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**.5

    def add_fleet(self,new_fleet,team): #adds a new fleet to the existing ships
        if team:
            for ship in new_fleet:
                self.ally_ships.append(ship)
        else:
            for ship in new_fleet:
                self.enemy_ships.append(ship)

    def refresh_ships(self,ally,enemy):
        self.ally_ships = []
        self.enemy_ships = []
        for ship in ally:
            self.ally_ships.append(ship)
        for ship in enemy:
            self.enemy_ships.append(ship)

    def update(self):
        'ENEMY SHIP AI'
        for ship in self.enemy_ships:
            ship.set_dest((ship.x+-50+random.randrange(100),ship.y-50+random.randrange(100)))
            if ship.x < 0:
                ship.set_dest((1000,500))
            if ship.x > 2000:
                ship.set_dest((1000,500))
            if ship.y < -500:
                ship.set_dest((1000,500))
            if ship.y > 1500:
                ship.set_dest((1000,500))
        self.make_lists()
        'ALLIED ATTACK'
        moving_list = [] #list of ships that are attacking
        for ship in self.ally_ships:
            if ship.task == 'ATTACK' and ship.state != 'Moving to position': #if ship is attacking and not forced moving, follow the nearest enemy
                ship.state = 'Moving to target'
                moving_list.append(ship)
        targets = self.move_attack_formation(len(moving_list),self.separation/2,self.enemy_ships[0].x,self.enemy_ships[0].y) #make list of target dests
        for i in range(len(moving_list)):
            target = targets[i]
            distance = self.distance((moving_list[i].x,moving_list[i].y),(self.enemy_ships[0].x,self.enemy_ships[0].y))
            if distance > moving_list[i].range:
                moving_list[i].in_range = False
            else:
                moving_list[i].in_range = True
                moving_list[i].attack_target_pos[0] = self.enemy_ships[0].x#set attack targets
                moving_list[i].attack_target_pos[1] = self.enemy_ships[0].y
                moving_list[i].attack_target = self.enemy_ships[0].id
            if distance>self.separation: #if out of range, move within range
                moving_list[i].state = 'Moving within range'
                moving_list[i].set_dest(target)
            elif distance < self.close_separation: #if it's too close
                moving_list[i].state = 'Moving away'
                moving_list[i].set_dest((moving_list[i].x-(target[0]-moving_list[i].x),moving_list[i].y-(target[1]-moving_list[i].y)))
            else: #if it's in its happy place
                moving_list[i].state = 'Aiming at target'
                moving_list[i].set_target_angle((self.enemy_ships[0].x,self.enemy_ships[0].y))
                moving_list[i].set_dest((moving_list[i].x,moving_list[i].y))

    def move_attack_formation(self,number,separation,destx,desty):
        targets = []
        if number == 0:
            angle = 0
        else:
            angle = 360/number
        for i in range(number): #angles at angle*i
            targets.append(tuple((destx+separation*np.cos(i*angle),(desty + separation * np.sin(i*angle)))))
        return targets

    def move_formation(self,number,separation,destx,desty): #produces a list of destination coordinates based on separation
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
