import pygame
import random
from scripts.helpers import *
from data.constants import *
from scripts.projectiles import *


DIRECTIONS = {
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
        self.sprites = {"default": load_image("entities/slime.png"),
                        "hurt": load_image("entities/slime_hurt.png")}
        self.health = 10
        self.movement_cooldown = 0
        self.damage = 10
        self.alive = True
        self.hit_flash = 0

        self.shoot_cooldown = 30


    def update(self, room):

        if self.movement_cooldown > 0:
            self.movement_cooldown -= 1

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.hit_flash > 0:
            self.hit_flash -= 1

        if self.shoot_cooldown == 0:
            self.shoot(room)

            self.shoot_cooldown = 120

        if self.movement_cooldown == 0:
            dx, dy = random.choice(list(DIRECTIONS.values()))
            self.pos[0] += dx * self.sprites["default"].get_width()
            self.pos[1] += dy * self.sprites["default"].get_height()
            self.movement_cooldown = 60

        slime_rect = self.hitbox() 

        for shot in room.shots:
            if shot.owner != "player" or shot.dying or not shot.alive:
                continue

            shot_rect = shot.hitbox()

            if slime_rect.colliderect(shot_rect):
                shot.kill()
                self.health -= shot.damage
                self.hit_flash = 4

        if self.health <= 0:
            self.alive = False




        
    def shoot(self, room):
        for direction in DIRECTIONS:
            proj = Shot((self.pos[0] + self.sprites["default"].get_width() // 2, self.pos[1] + self.sprites["default"].get_height() // 2), "slime", DIRECTIONS[direction], "proj1", self.screen)
            proj.damage = self.damage
            room.shots.append(proj)


    def draw(self):
        if self.hit_flash > 0:
            self.screen.blit(self.sprites["hurt"], self.pos)
        else:
            self.screen.blit(self.sprites["default"], self.pos)


    def bottom(self):
        return self.pos[1] + self.sprites["default"].get_height()

    def hitbox(self):
        return self.sprites["default"].get_rect(topleft=self.pos)