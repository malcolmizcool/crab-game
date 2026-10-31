import pygame
from scripts.helpers import *
from data.constants import *

class Shot:
    def __init__(self, pos, owner, direction, type, screen):
        self.pos = list(pos)
        self.direction = direction
        self.screen = screen
        self.owner = owner
        self.type = type

        self.speed = 1.5
        self.damage = 3
        self.size = 1
        self.range = 45

        self.time_active = 0

        self.inherited = (0, 0)
        
        
        self.asset = load_image("projectiles/" + self.type + ".png")
        self.death_assets = load_images("projectiles/" + self.type + "_death")
        
        self.spectral = False
        self.homing = False

        self.alive = True
        self.dying = False
        self.death_frame = 0

        self.modifiers = []

    def update(self, solids):
        self.time_active += 1

        if self.range <= self.speed * self.time_active:
            self.kill()

        if self.dying:
            self.death_frame += 1
            if self.death_frame >= len(self.death_assets):
                self.alive = False
            return 

        self.pos[0] += self.direction[0] * self.speed + self.inherited[0]
        self.pos[1] += self.direction[1] * self.speed + self.inherited[1]

        if self.pos[0] > SCREEN_WIDTH + 10 or self.pos[0] < -10 or self.pos[1] > SCREEN_HEIGHT + 10 or self.pos[1] < -10:
            self.show_death_animation = True
            self.alive = False

        for modifier in self.modifiers:
            modifier.update(self)

        if not self.spectral:
            for solid in solids:
                if self.hitbox().colliderect(solid):
                    self.kill()
                    break
                        



    def draw(self):
        if self.dying:
            image = self.death_assets[self.death_frame]
        else:
            image = self.asset
        self.screen.blit(image, (self.pos[0], self.pos[1]))

    def kill(self):
        self.dying = True

    def hitbox(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.asset.get_width(), self.asset.get_height())