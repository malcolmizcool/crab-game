import pygame

from scripts.helpers import *

class GameOver:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

    def run(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game.new_game()

    def draw(self):
        pass