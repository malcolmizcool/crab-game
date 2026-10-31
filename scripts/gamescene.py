import pygame
from scripts.player import *
from scripts.floor import *
from scripts.chat import ChatLog

class GameScene:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.chat = ChatLog(screen)
        self.player = Player(game, screen, self)
        self.floor = Floor(game, screen)

    def run(self, events):
        self.screen.fill((54, 60, 66))



        room = self.floor.current_room()
        room.update()
        self.player.update(events, room)

        for direction, door in room.door_hitboxes.items():
            if self.player.hitbox().colliderect(door):
                self.floor.enter_room(direction, self.player)
                break

        self.chat.update()

        self.floor.current_room().draw(self.player)
        self.chat.draw()

