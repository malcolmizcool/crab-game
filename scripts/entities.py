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

class Entity:
    def __init__(self, pos, game, screen, animations):
        self.pos = list(pos)
        self.game = game
        self.screen = screen
        self.animations = animations
        self.size = animations["default"].img().get_size()

        self.alive = True
        self.room = None                    
        self.hitbox_offset = (0, 0, 0, 0)
        self.health = 1

        self.hit_flash = 0
        self.facing = "default"
        self.invincible = 0
        self.invincibility_time = 0         
        self.dying = False

        self.action = ""
        self.set_action("default")

    def set_action(self, action):
        if action not in self.animations:
            action = "default"
        if action != self.action:
            self.action = action
            self.animation = self.animations[action].copy()

    def choose_action(self):
        if self.dying:
            return "death"
        return self.facing

    def bottom(self):
        return self.pos[1] + self.size[1]

    def update(self, room):
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.invincible > 0:
            self.invincible -= 1

        self.set_action(self.choose_action())
        self.animation.update()

        if self.dying and self.animation.done:
            self.on_death_finished()

    def take_damage(self, amount):

        if self.dying or self.invincible > 0:
            return

        self.health -= amount
        self.hit_flash = 4
        self.invincible = self.invincibility_time
        if self.health <= 0:
            self.start_dying()

    def start_dying(self):
        self.dying = True
        if "death" in self.animations:
            self.set_action("death")
        else:
            self.on_death_finished()

    def on_death_finished(self):
        self.alive = False
        

    def hitbox(self):
        l, t, r, b = self.hitbox_offset
        return pygame.FRect(self.pos[0] + l, self.pos[1] + t,
                            self.size[0] - l - r, self.size[1] - t - b)

    def center(self):
        return (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

    def current_sprite(self):
        if self.hit_flash > 0 and not self.dying and "hurt" in self.animations:
            return self.animations["hurt"].img()
        return self.animation.img()

    def draw(self):
        self.screen.blit(self.current_sprite(), self.pos)

    def move(self, dx, dy, room):
        hit = {"left": False, "right": False, "up": False, "down": False}
        l, t, _, _ = self.hitbox_offset

        self.pos[0] += dx
        rect = self.hitbox()
        for solid in room.solid_rects():
            if rect.colliderect(solid):
                if dx > 0:
                    rect.right = solid.left
                    hit["right"] = True
                elif dx < 0:
                    rect.left = solid.right
                    hit["left"] = True
                self.pos[0] = rect.x - l

        self.pos[1] += dy
        rect = self.hitbox()
        for solid in room.solid_rects():
            if rect.colliderect(solid):
                if dy > 0:
                    rect.bottom = solid.top
                    hit["down"] = True
                if dy < 0:
                    rect.top = solid.bottom
                    hit["up"] = True
                self.pos[1] = rect.y - t

        return hit


class Slime(Entity):
    def __init__(self, pos, game, screen):

        super().__init__(pos, game, screen, {
            "default": Animation([load_image("entities/slime.png")]),
            "hurt": Animation([load_image("entities/slime_hurt.png")])
        })

        self.health = 10
        self.movement_cooldown = 0
        self.damage = 0
        self.shoot_cooldown = random.randint(30, 100)


    def update(self, room):

        super().update(room)
        if self.dying:
            return
        
        if self.movement_cooldown > 0:
            self.movement_cooldown -= 1

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.shoot_cooldown == 0:
            self.shoot(room)

            self.shoot_cooldown = 120

        if self.movement_cooldown == 0:
            dx, dy = random.choice(list(DIRECTIONS.values()))
            self.pos[0] += dx * self.size[0]
            self.pos[1] += dy * self.size[1]
            self.movement_cooldown = 60


        for shot in room.shots:
            if shot.owner != "player" or shot.dying or not shot.alive:
                continue
            if self.hitbox().colliderect(shot.hitbox()):
                shot.kill()
                self.take_damage(shot.damage)


        
    def shoot(self, room):
        for direction in DIRECTIONS.values():
            proj = Shot(self.center(), "slime", direction, "proj1", self.screen)
            proj.damage = self.damage
            room.shots.append(proj)


    def on_death_finished(self):
        super().on_death_finished()
        # four diagonal shots when the slime dies
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            proj = Shot(self.center(), "slime", direction, "proj1", self.screen)
            proj.damage = self.damage
            self.room.shots.append(proj)

