import pygame
from scripts.helpers import *

class Shot:
    def __init__(self, pos, direction, screen):
        self.pos = list(pos)
        self.direction = direction
        self.screen = screen
        self.speed = 1.1
        self.damage = 3
        self.size = 1
        self.homing = False
        self.alive = True
        self.asset = load_image("projectiles/sand_ball.png")


    def update(self):
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

        self.draw()


    def draw(self):
        self.screen.blit(self.asset, (self.pos[0], self.pos[1]))