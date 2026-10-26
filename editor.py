import pygame
from data.constants import *

class LevelEditor:
    def __init__(self, game):
        self.showInventory = False
        self.game = game

    def run(self, events):
        

        if self.showInventory:
            self.game.screen.fill((0, 255, 255))
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.showInventory = False
        else:
            self.game.screen.fill((255, 0, 255))
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.showInventory = True