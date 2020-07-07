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
        self.separation = BEAM_RANGE -50
        self.close_separation = BEAM_RANGE/2

    def l_click(self,mouse_pos):
        self.make_lists()

    def print(self):
        output = ''
        for ship in self.ally_ships:
            output += str(ship)
        for ship in self.enemy_ships:
            output += str(ship)

    def make_lists(self):
        self.attacking = (x for x in self.ally_ships if (x.selected and x.task == 'ATTACK')) #list of ships that are selected & attacking
        self.evading = (x for x in self.ally_ships if (x.selected and x.task == 'HOLD')) #list of ships that are selected & evading
        self.ignoring = (x for x in self.ally_ships if (x.selected and x.task == 'IGNORE')) #list of ships that are selected & ignoring
        self.retreating = (x for x in self.ally_ships if (x.selected and x.task == 'RETREAT')) #list of ships that are selected & retreating
        self.selected = (x for x in self.ally_ships if (x.selected)) #list of selected ships

    def r_click(self,mouse_pos): #handles if user right clicks
        clicked_enemy = False
        selected_list = []
        for ship in self.selected:
            selected_list.append(ship)
        'if r-clicks an enemy, set it as the selected ships target'
        for ship in self.enemy_ships:
            if ship.rect.collidepoint(self.game.camera.apply_point(mouse_pos)): #if you right click an enemy ship
                clicked_enemy = True
                for ally_ship in selected_list:
                    ally_ship.target_ship_id = ship.id
                    ally_ship.task = 'ATTACK'
                    ally_ship.state = 'idle'

        if not clicked_enemy:
            'moves selected ally ships in a formation to wherever is clicked'
            self.make_lists()
            targets = self.move_formation(len(selected_list),30,mouse_pos[0],mouse_pos[1]) #make list of target dests
            for i in range(len(selected_list)):
                target = self.game.camera.apply_point(targets[i])
                selected_list[i].set_dest(target)
                selected_list[i].state = 'Moving to position'

    def find_closest(self,start_ship,start_team):
        closest = 9999
        output = None
        if start_team: # if its an ally we're find the closest of
            for ship in self.enemy_ships:
                dist = self.distance((start_ship.x,start_ship.y),(ship.x,ship.y))
                if dist < closest:
                    closest = dist
                    output = ship
        else: #if its an enemy, searches allies for closest ship
            for ship in self.ally_ships:
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
        random.seed()
        'ENEMY SHIP AI'
        'movement'
        alive_count = 0
        for ship in self.game.enemy_ships:
            if ship.alive == True:
                alive_count += 1
        if alive_count > 0:
            for fleet in self.game.enemy_fleets: #creates all enemy fleets
                fleet_list = []
                fleet_leader = ''
                leader_found = False
                for ship in self.enemy_ships: #creates the fleet list
                    if ship.fleet == fleet:
                        fleet_list.append(ship)
                        if ship.leader: #sets the leader of the fleet
                            fleet_leader = ship
                            leader_found = True
                if not leader_found:
                    fleet_list[0].leader = True
                    fleet_leader = fleet_list[0]

                targets = self.move_enemy_circle(len(fleet_list)-1,100,tuple((fleet_leader.x,fleet_leader.y)))
                target_index = 0
                for i in range(len(fleet_list)):
                    if not fleet_list[i].leader: #if its a regular ship
                        fleet_list[i].set_dest(targets[target_index])
                        target_index += 1

                fleet_leader.set_dest((fleet_leader.x+-50+random.randrange(100),fleet_leader.y-50+random.randrange(100)))
                if fleet_leader.x < 0:
                    fleet_leader.set_dest((1000,500))
                if fleet_leader.x > 2000:
                    fleet_leader.set_dest((1000,500))
                if fleet_leader.y < -500:
                    fleet_leader.set_dest((1000,500))
                if fleet_leader.y > 1500:
                    fleet_leader.set_dest((1000,500))
        'enemy attacking'
        for i in range(len(self.enemy_ships)):
            target_ship = self.find_closest(self.enemy_ships[i],False)
            distance = self.distance((self.enemy_ships[i].x,self.enemy_ships[i].y),(target_ship.x,target_ship.y)) #distance from ally ship to enemy
            pg.draw.rect(self.game.screen,WHITE,pg.Rect(10,10,10,10))
            if distance < self.enemy_ships[i].range:
                self.enemy_ships[i].in_range = True
                self.enemy_ships[i].attack_target = target_ship.id
                self.enemy_ships[i].attack_target_pos[0] = target_ship.x
                self.enemy_ships[i].attack_target_pos[1] = target_ship.y
            else:
                self.enemy_ships[i].in_range = False

        self.make_lists()
        'ALLIED SHIP AI'
        '-----------HOLD-----------'
        for ship in self.ally_ships:
            if ship.task == 'HOLD':
                ship.destx = ship.x #stop moving
                ship.desty = ship.y
                ship.state = 'Holding'
        if len(self.enemy_ships) > 0: #if there are enemy ships left
            self.game.enemy_exists = True
            moving_list = [] #list of ships that are attacking
            for ship in self.ally_ships:
                if (ship.task == 'ATTACK' or ship.task == 'RETREAT') and ship.state != 'Moving to position': #if ship is attacking and not forced moving, follow the nearest enemy
                    ship.state = 'Moving to target'
                    moving_list.append(ship)
            for i in range(len(moving_list)):
                #override target if right clicked
                target_ship = self.find_closest(moving_list[i],True)
                for enemy_ship in self.enemy_ships:
                    if enemy_ship.id == moving_list[i].target_ship_id:
                        if enemy_ship.alive: #if target is killed, reset it to 0
                            target_ship = enemy_ship
                        else:
                            moving_list[i].target_ship_id = 0
                '-----------RETREAT-----------'
                if moving_list[i].task == 'RETREAT':
                    distance = self.distance((moving_list[i].x,moving_list[i].y),(target_ship.x,target_ship.y)) #distance from ally ship to enemy
                    moving_list[i].state = 'Retreating'
                    if distance < 500:
                        moving_list[i].set_dest((moving_list[i].x-(target_ship.x-moving_list[i].x),moving_list[i].y-(target_ship.y-moving_list[i].y)))
                elif moving_list[i].task == 'ATTACK':
                    '-----------ATTACK-----------'
                    target  = self.move_attack_formation(i,self.separation/2,target_ship.x,target_ship.y) #create targets when attacking
                    distance = self.distance((moving_list[i].x,moving_list[i].y),(target_ship.x,target_ship.y)) #distance from ally ship to enemy
                    if distance > moving_list[i].range:
                        moving_list[i].in_range = False #if out of range
                    else:
                        moving_list[i].in_range = True
                        moving_list[i].attack_target_pos[0] = target_ship.x#set attack targets
                        moving_list[i].attack_target_pos[1] = target_ship.y
                        moving_list[i].attack_target = target_ship.id
                    if distance>self.separation: #if out of range, move within range
                        moving_list[i].state = 'Moving within range'
                        moving_list[i].set_dest(target)
                    elif distance < self.close_separation: #if it's too close
                        moving_list[i].state = 'Moving away'
                        moving_list[i].set_dest((moving_list[i].x-(target_ship.x-moving_list[i].x),moving_list[i].y-(target_ship.y-moving_list[i].y)))
                    else: #if it's in its happy place
                        moving_list[i].state = 'Aiming at target'
                        moving_list[i].set_target_angle((target_ship.x,target_ship.y))
                        moving_list[i].set_dest((moving_list[i].x,moving_list[i].y))
        else: #if there are no enemy ships left
            for ship in self.game.ally_ships:
                self.state = 'Idle'
                self.game.enemy_exists = False
    def move_enemy_circle(self,number,separation,leader_pos):
        output = []
        if number > 0:
            angle = 360/number
        else:
            angle = 0
        for i in range(number):
            rad_angle = angle*i*np.pi/180
            output.append(tuple((leader_pos[0]+separation*np.cos(rad_angle),leader_pos[1]+separation*np.sin(rad_angle))))
        return output

    def move_attack_formation(self,seed,separation,destx,desty):
        random.seed(seed*1000)
        angle = -50 + random.randrange(101)
        return tuple((destx+separation*np.cos(angle),(desty + separation * np.sin(angle))))

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
