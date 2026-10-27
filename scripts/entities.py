import pygame
import random
from scripts.helpers import *

MOVEMENT_DIRECTIONS = {
    "up": (0, -1),
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0)
}

class Slime:
    def __init__(self, pos, game, screen):

        self.pos = list(pos)
        self.game = game
        self.screen = screen
        self.sprite = load_image("entities/slime1.png")
        self.health = 10
        self.movement_cooldown = 0
        self.damage = 1


    def update(self):

        if self.movement_cooldown > 0:
            self.movement_cooldown -= 1

        if self.movement_cooldown == 0:
            random_choice = random.choice(MOVEMENT_DIRECTIONS)
            self.pos[0] = random_choice[0] * self.sprite.get_width()
            self.pos[1] = random_choice[1] * self.sprite.get_height()

        self.draw()

        


    def draw(self):
        self.screen.blit(self.sprite, self.pos)