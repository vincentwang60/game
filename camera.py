import pygame as pg
import numpy as np
from settings import *

class camera():
    def __init__(self):
        self.x = 0
        self.dx = 0
        self.dy = 0
        self.y = 0
        self.state = pg.Rect(self.x, self.y, WIDTH, HEIGHT)

    def apply(self, target):
        return target.rect.move(self.state.topleft[0],self.state.topleft[1])

    def apply_rect(self, target):
        return target.move(-self.state.topleft[0],-self.state.topleft[1])
    def apply_point(self,target):
        out_x = target[0]-self.state.topleft[0]
        out_y = target[1]-self.state.topleft[1]
        return (out_x,out_y)

    def apply_opp(self,target):
        out_x = target[0]+self.state.topleft[0]
        out_y = target[1]+self.state.topleft[1]
        return (out_x,out_y)

    def move(self):
        if (self.x > (WIDTH-MAP_SIZE[0])/2 and self.dx < 0) or (self.x < (MAP_SIZE[0]-WIDTH)/2 and self.dx > 0):
            self.x += self.dx
        if (self.y > (HEIGHT-MAP_SIZE[1])/2 and self.dy < 0) or (self.y < (MAP_SIZE[1]-HEIGHT)/2 and self.dy > 0):
            self.y += self.dy

    def update(self,states):
        self.dx = 0
        self.dy = 0
        if states[0]:
            self.dy = SCROLL_SPEED
        if states[1]:
            self.dx = SCROLL_SPEED
        if states[2]:
            self.dy = -SCROLL_SPEED
        if states[3]:
            self.dx = -SCROLL_SPEED
        self.state = pg.Rect(self.x, self.y, WIDTH, HEIGHT)
        self.move()
