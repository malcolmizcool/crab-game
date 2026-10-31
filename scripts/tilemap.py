import pygame
from scripts.helpers import *
from data.constants import *
import json

SOLID_TILES = {'rock', 'fol'}
IGNORE_TILES = {'spawner'}

class Tile:
    def __init__(self, game, screen, type, variant, gpos, collision, sprite):
        self.game = game
        self.screen = screen
        self.type = type
        self.variant = variant
        self.pos = gpos
        self.tile_size = TILE
        self.collision = collision
        self.sprite = sprite
        self.rect = pygame.Rect(self.pos[0] * self.tile_size + 1, self.pos[1] * self.tile_size + 2, self.sprite.get_width() - 1, self.sprite.get_height() - 2)
        self.alive = True

    def draw(self):
        if self.alive:
            self.screen.blit(self.sprite, (self.pos[0] * self.tile_size, self.pos[1] * self.tile_size))

    def bottom(self):
        return self.pos[1] * self.tile_size + self.sprite.get_height()

    def hitbox(self):
        return self.rect


class Tilemap:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.tilemap = {}
        self.tile_size = TILE
        
        self.assets = {
            'rock': load_images('tiles/rock'),
            'wood': load_images('tiles/wood'),
            'fol': load_images('tiles/fol'),
            'spawner': [load_image('editor/spawner.png')]  

        }


    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']

    def render(self, surf, offset=(0, 0)):
        for tile in self.tilemap.values():
            img = self.assets[tile['type']][tile['variant']]
            surf.blit(img, (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

    def build_tiles(self):
        tiles = []
        for tile in self.tilemap.values():
            if tile['type'] in IGNORE_TILES:
                continue       
            sprite = self.assets[tile['type']][tile['variant']]
            tiles.append(Tile(self.game, self.screen, tile['type'], tile['variant'], tile['pos'], tile['type'] in SOLID_TILES, sprite))
        return tiles

    def spawners(self):
        return [(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size)
                for tile in self.tilemap.values() if tile['type'] == 'spawner']

    def extract(self, id_pairs, keep=False):
        matches = []
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    