import pygame
from data.constants import *
from scripts.helpers import *
from scripts.tilemap import *

class LevelEditor:
    def __init__(self, game, screen):
        self.showInventory = False
        self.game = game
        self.screen = screen

        self.tilemap = Tilemap(self.game, self.screen)
        self.assets = self.tilemap.assets       # {type: [variant images]}

        self.tile_list = list(self.assets)
        self.tile_group = 0                     # which type (rock, wood...)
        self.tile_variant = 0                   # which image within that type
        self.clicking = False
        self.right_clicking = False

        try:
            self.tilemap.load('map.json')
        except:
            pass

    def run(self, events):
        self.screen.fill((59, 74, 97))
        current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
        current_tile_img.set_alpha(100)

        self.screen.blit(current_tile_img, (5, 5))

        mpos = self.game.mouse_pos()
        tile_pos = (mpos[0] // TILE, mpos[1] // TILE)

        if self.clicking:
            self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
        if self.right_clicking:
            tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
            if tile_loc in self.tilemap.tilemap:
                del self.tilemap.tilemap[tile_loc]


        self.screen.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size))
        self.tilemap.render(self.screen)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True
                if event.button == 3:
                    self.right_clicking = True
                if event.button in (4, 5):
                    step = -1 if event.button == 4 else 1
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # shift + scroll: cycle variants of the current type
                        variants = len(self.assets[self.tile_list[self.tile_group]])
                        self.tile_variant = (self.tile_variant + step) % variants
                    else:
                        # scroll: change type, starting at its first variant
                        self.tile_group = (self.tile_group + step) % len(self.tile_list)
                        self.tile_variant = 0

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                if event.button == 3:
                    self.right_clicking = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    self.tilemap.save('map.json')