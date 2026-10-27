import pygame
from scripts.helpers import *

class Tile:
    def __init__(self, game, screen, type, variant, gpos, collision):
        self.game = game
        self.screen = screen
        self.type = type
        self.variant = variant
        self.pos = gpos
        self.tile_size = 16
        self.collision = collision
        self.sprite = load_image('tiles/' + str(type) + '/' + str(variant) + '.png')
        self.rect = pygame.Rect(self.pos[0] * self.tile_size + 1, self.pos[1] * self.tile_size + 4, self.sprite.get_width() - 2, self.sprite.get_height() - 4)
        self.alive = True

    def draw(self):
        if self.alive:
            self.screen.blit(self.sprite, (self.pos[0] * self.tile_size, self.pos[1] * self.tile_size))

    def bottom(self):
        return self.pos[1] * self.tile_size + self.sprite.get_height()

    def hitbox(self):
        return self.rect