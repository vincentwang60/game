import pygame as pg
import numpy as np
from settings import *
import math

class ship_mngr(): #issues move commands to ships
    def __init__(self,game):
        self.game = game
        'VARIABLES'
        self.ally_ships = []
        self.enemy_ships = []

    def r_click(self,mouse_pos): #handles if user right clicks
        attack = (x for x in self.ally_ships if (x.selected and x.task == 'ATTACK')) #list of ships that are selected & attacking
        evading = (x for x in self.ally_ships if (x.selected and x.task == 'EVADE')) #list of ships that are selected & evading
        ignoring = (x for x in self.ally_ships if (x.selected and x.task == 'IGNORE')) #list of ships that are selected & ignoring
        retreating = (x for x in self.ally_ships if (x.selected and x.task == 'RETREAT')) #list of ships that are selected & retreating
        'IGNORE'
        ignoring_list = []
        for x in ignoring:
            ignoring_list.append(x)
        targets = self.move_formation(len(ignoring_list),30,mouse_pos[0],mouse_pos[1],'IGNORE') #make list of target dests
        for i in range(len(ignoring_list)):
            target = self.game.camera.apply_point(targets[i])
            ignoring_list[i].set_dest(target)
        'ATTACK'

    def add_fleet(self,new_fleet,team): #adds a new fleet to the existing ships
        if team:
            for ship in new_fleet:
                self.ally_ships.append(ship)
        else:
            for ship in new_fleet:
                self.enemy_ships.append(ship)

    def update(self):
        targets = []
        for ship in self.enemy_ships:
            if ship.x > 0:
                ship.set_dest((0,ship.y))
            else:
                ship.set_dest((1920,ship.y))
            ship.set_dest((100,100))
        return targets

    def move_formation(self,number,separation,destx,desty,stance): #produces a list of destination coordinates based on separation
        targets = []
        if stance == 'IGNORE':
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
