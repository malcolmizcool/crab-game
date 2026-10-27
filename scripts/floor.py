import pygame
from scripts.entities import *
from scripts.tilemap import *

class Floor:
    def __init__(self, game, screen):
        self.rooms = {(0, 0): Room(game, screen)}
        self.current = (0, 0)

    def current_room(self):
        return self.rooms[self.current]


class Room:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.enemies = []
        self.shots = []
        self.pickups = []
        self.cleared = False
        self.visited = False
        self.doors = {}
        self.loaded_tiles = {'1;1': {'type': 'rock', 'variant': 1, 'pos': (1, 1)}}
        self.tilemap = []

        for tile in self.loaded_tiles.values():
            new_tile = Tile(self.game, self.screen, tile['type'], tile['variant'], tile['pos'], True)
            self.tilemap.append(new_tile)

    def update(self):
        for shot in self.shots:
            shot.update(self.tilemap)
        for enemy in self.enemies:
            enemy.update(self)

        self.enemies = [e for e in self.enemies if e.alive]
        self.shots = [s for s in self.shots if s.alive]



        


    def spawn_enemies(self):
        self.enemies.append(Slime((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), self.game, self.screen))

    def draw(self, player):
        things = self.enemies + [player] + self.tilemap
        things.sort(key=lambda thing: thing.bottom())
        for thing in things:
            thing.draw()

        
        for shot in self.shots:
            shot.draw()

        if self.game.debugState:
            self.draw_hitboxes(player)

    def draw_hitboxes(self, player):
        pygame.draw.rect(self.screen, (0, 255, 0), player.hitbox(), 1)
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (0, 255, 0), enemy.hitbox(), 1)
        for tile in self.tilemap:
            pygame.draw.rect(self.screen, (0, 255, 0), tile.hitbox(), 1)
        for shot in self.shots:
            pygame.draw.rect(self.screen, (0, 255, 0), shot.hitbox(), 1)