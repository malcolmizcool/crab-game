from data.items import ITEMS
from scripts.effects import EFFECTS
from scripts.helpers import *
from scripts.particle import Particle

import math
import random

MAX_QUALITY = 4           

class Item:
    def __init__(self, id):

        self.id = id
        self.data = ITEMS[self.id]

        self.name = self.data["name"]
        self.stats = self.data.get("stats", {})
        self.flags = self.data.get("flags", [])
        self.quality = self.data["quality"]
        self.effects = [EFFECTS[name]() for name in self.data.get("effects", [])]

    def on_pickup(self, player):
        for stat, amount in self.stats.items():
            player.stats[stat] += amount

        player.game.send_chat(f"New item: {self.name} - {self.data["tooltip"]}")

    def on_shoot(self, player, shot):
        for flag in self.flags:
            setattr(shot, flag, True)
        for effect in self.effects:
            effect.on_shoot(player, shot)

    def on_hit(self, player, shot):
        for effect in self.effects:
            if effect.on_hit(player, shot):
                return True
        return False


class ItemPickup:
    def __init__(self, id, pos, game, screen):
        self.item = Item(id)
        self.pos = list(pos)
        self.game = game
        self.screen = screen

        self.image = load_image(ITEMS[id]["sprite"])
        self.alive = True

        self.quality = self.item.quality
        self.particles = []         
        self.room = None            

    def update(self):

        if random.random() < (self.quality / MAX_QUALITY) ** 2:
            hitbox = self.hitbox()
            pos = (hitbox.x + random.random() * hitbox.width, hitbox.y + random.random() * hitbox.height)
            self.particles.append(Particle(self.game, 'item_glow/' + str(self.quality), pos,
                                           velocity=[random.uniform(-1, 1), random.uniform(-1, 1)]))

        for particle in self.particles.copy():
            if particle.update():
                self.particles.remove(particle)


    def hitbox(self):
        return self.image.get_rect(topleft=self.pos)

    def bottom(self):
        return self.pos[1] + self.image.get_height()

    def collect(self, player):
        player.add_item(self.item)
        self.alive = False
        if self.room:
            self.room.particles.extend(self.particles)
        self.particles = []

    def draw_glow(self):
        for particle in self.particles:
            particle.render(self.screen)

    def draw(self):
        bob = math.sin(pygame.time.get_ticks() / 300) * 1.5
        self.screen.blit(self.image, (self.pos[0], self.pos[1] + bob))