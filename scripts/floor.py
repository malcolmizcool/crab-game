import pygame
from scripts.entities import *
from scripts.tilemap import *
from data.constants import *
import json
from scripts.item_script import *
from scripts.particle import *

DOOR_SIZE = 32
DOOR_DEPTH = 8

CX = SCREEN_WIDTH // 2
CY = SCREEN_HEIGHT // 2

DOOR_RECTS = {
    (1, 0):  pygame.Rect(SCREEN_WIDTH - DOOR_DEPTH, CY - DOOR_SIZE // 2, DOOR_DEPTH, DOOR_SIZE),
    (-1, 0): pygame.Rect(0, CY - DOOR_SIZE // 2, DOOR_DEPTH, DOOR_SIZE),
    (0, -1): pygame.Rect(CX - DOOR_SIZE // 2, 0, DOOR_SIZE, DOOR_DEPTH),
    (0, 1):  pygame.Rect(CX - DOOR_SIZE // 2, SCREEN_HEIGHT - DOOR_DEPTH, DOOR_SIZE, DOOR_DEPTH),
}
ENTRY_POINTS = {
    (1, 0):  (WALL + 2, CY - 6),                        
    (-1, 0): (SCREEN_WIDTH - WALL - 13, CY - 6),        
    (0, -1): (CX - 5, SCREEN_HEIGHT - WALL - 14),       
    (0, 1):  (CX - 5, WALL + 2),                        
}

class Floor:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

        self.layout = {
            (0, 0): "data/stage1/rooms/001.json",
            (1, 0): "data/stage1/rooms/002.json"
        }

        self.rooms = {}
        self.current = (0, 0)
        self.build_room((0, 0))
        self.rooms[(0, 0)].on_enter()

    def build_room(self, pos):
        doors = [d for d in DOOR_RECTS if (pos[0] + d[0], pos[1] + d[1]) in self.layout]
        self.rooms[pos] = Room(self.game, self.screen, self.layout[pos], doors)

    def current_room(self):
        return self.rooms[self.current]

    def enter_room(self, direction, player):
        new_pos = (self.current[0] + direction[0], self.current[1] + direction[1])
        if new_pos not in self.rooms:
            self.build_room(new_pos)
        self.current = new_pos
        self.rooms[new_pos].on_enter()
        player.pos = list(ENTRY_POINTS[direction])


class Room:
    def __init__(self, game, screen, layout_path, door_directions):
        self.game = game
        self.screen = screen
        self.enemies = []
        self.shots = []
        self.pickups = []
        self.particles = []
        self.cleared = False
        self.visited = False

        tilemap = Tilemap(game, screen)
        tilemap.load(layout_path)
        self.tiles = tilemap.build_tiles()

        self.door_hitboxes = {}
        for direction in door_directions:
            self.door_hitboxes[direction] = DOOR_RECTS[direction]

        self.walls = [pygame.Rect(-WALL, -WALL, SCREEN_WIDTH + 2 * WALL, WALL),   # top
                      pygame.Rect(-WALL, 0, WALL, SCREEN_HEIGHT),                  # left
                      pygame.Rect(SCREEN_WIDTH, 0, WALL, SCREEN_HEIGHT),           # right
                      pygame.Rect(-WALL, SCREEN_HEIGHT, SCREEN_WIDTH + 2 * WALL, WALL)]  # bottom

        self.enemy_spawns = tilemap.spawners()


    def on_enter(self):
        if not self.visited:
            self.visited = True
            for pos in self.enemy_spawns:
                self.add_enemy(Slime(pos, self.game, self.screen))



    def update(self):
        for shot in self.shots:
            shot.update(self.solid_rects())
        for enemy in self.enemies:
            enemy.update(self)

        self.enemies = [e for e in self.enemies if e.alive]
        self.shots = [s for s in self.shots if s.alive]

        

        for particle in self.particles.copy():
            kill = particle.update()
            if kill:
                self.particles.remove(particle)

        for pickup in self.pickups:
            pickup.update()


    def add_enemy(self, enemy):
        enemy.room = self
        self.enemies.append(enemy)

    def add_pickup(self, pickup):
        pickup.room = self
        self.pickups.append(pickup)

    def spawn_enemies(self):
        self.add_enemy(Slime((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), self.game, self.screen))

    def draw(self, player):
        things = self.enemies + [player] + self.tiles + self.pickups
        things.sort(key=lambda thing: thing.bottom())
        for thing in things:
            thing.draw()

        # item glow goes over the room, then each item is drawn again over its own glow
        for pickup in self.pickups:
            pickup.draw_glow()
            pickup.draw()

        for shot in self.shots:
            shot.draw()

        for particle in self.particles:
            particle.render(self.screen)

        if self.game.debugState:
            self.draw_hitboxes(player)

    def draw_hitboxes(self, player):
        pygame.draw.rect(self.screen, (0, 255, 0), player.hitbox(), 1)
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (0, 255, 0), enemy.hitbox(), 1)
        for tile in self.tiles:
            pygame.draw.rect(self.screen, (0, 255, 0), tile.hitbox(), 1)
        for door in self.door_hitboxes.values():
            pygame.draw.rect(self.screen, (0, 0, 255), door, 1)
        for shot in self.shots:
            pygame.draw.rect(self.screen, (0, 255, 0), shot.hitbox(), 1)


    def solid_rects(self):
        rects = list(self.walls)
        rects += [t.hitbox() for t in self.tiles if t.collision and t.alive]
        return rects
        