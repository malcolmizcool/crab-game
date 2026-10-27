import pygame
from scripts.player import *
from scripts.floor import *

class GameScene:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.player = Player(game, screen)
        self.floor = Floor(game, screen)

    def run(self, events):
        self.screen.fill((54, 60, 66))



        room = self.floor.current_room()
        room.update()
        self.player.update(events, room)
        room.draw(self.player)