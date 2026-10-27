import pygame
from scripts.helpers import *
from scripts.projectiles import *

SHOOT_DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_RIGHT: (1, 0),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
}

class Player:
    def __init__(self, game, screen):
        self.pos = [50, 50]
        self.items = []
        self.game = game
        self.screen = screen
        self.stats = {
            "health": 6,
            "velocity": [0, 0],
            "speed": 0.5,
            "damage": 3,
            "fire_rate": 30,
            "shot_speed": 1.5,
            "range": 45,
            "coins": 0,
        }
        self.movement = [False, False, False, False]
        self.sprites = {"right": load_image("player/char_right.png"),
                        "left": load_image("player/char_left.png"),
                        "up": load_image("player/char_up.png"),
                        "default": load_image("player/char_default.png")}

        self.shot_cooldown = 0

        self.dying = False
        self.death_assets = load_images('player/char_death')
        self.death_frame = 0




    def update(self, events, room):

        if self.dying:
            
            if self.death_frame < len(self.death_assets) - 1:
                self.death_frame += 1 
            else:
                self.game.screenState = "gameover"
            return
#--------------------------------------------------------------------------------
        for event in events:                                   #movement logic etc etc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_s:
                    self.movement[2] = True
                if event.key == pygame.K_a:
                    self.movement[3] = True


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_s:
                    self.movement[2] = False
                if event.key == pygame.K_a:
                    self.movement[3] = False



        x_input = self.movement[1] - self.movement[3]
        y_input = self.movement[2] - self.movement[0]
        self.frame_movement = (x_input * self.stats["speed"] + self.stats["velocity"][0],
                          y_input * self.stats["speed"] + self.stats["velocity"][1])


        
#---------------------------------------------------------------------------------

        if self.shot_cooldown > 0:                              #shot logic etc etc
            self.shot_cooldown -= 1

        keys = pygame.key.get_pressed()
        for key, direction in SHOOT_DIRECTIONS.items():
            if keys[key] and self.shot_cooldown == 0:
                self.shoot(direction, room)
                self.shot_cooldown = self.stats["fire_rate"]
                break

#-------------------------------------------------------------------- 
# collision logic

#tiles
        self.pos[0] += self.frame_movement[0]
        rect = self.hitbox()
        for tile in room.tilemap:
            if tile.collision and tile.alive:
                if rect.colliderect(tile.rect):
                    if self.frame_movement[0] > 0:
                        rect.right = tile.rect.left
                    if self.frame_movement[0] < 0:
                        rect.left = tile.rect.right
                    self.pos[0] = rect.x - 2

        self.pos[1] += self.frame_movement[1]
        rect = self.hitbox()
        for tile in room.tilemap:
            if tile.collision and tile.alive:
                if rect.colliderect(tile.rect):
                    if self.frame_movement[1] > 0:
                        rect.bottom = tile.rect.top
                    if self.frame_movement[1] < 0:
                        rect.top = tile.rect.bottom
                    self.pos[1] = rect.y - 4
# other projectiles

        for shot in room.shots:
            if shot.owner == "player" or shot.dying or not shot.alive:
                continue 
            shot_rect = shot.hitbox()
            player_rect = self.hitbox()

            if player_rect.colliderect(shot_rect):
                self.stats["health"] -= shot.damage
                shot.kill()


#--------------------------------------------------------------------------
#other
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                room.spawn_enemies()

        if self.stats["health"] <= 0:
            self.dying = True
                


#---------------------------------------------------------------------------

    def shoot(self, direction, room):
        shot = Shot((self.pos[0] + self.sprites["right"].get_width() // 2 - 2, self.pos[1] + self.sprites["right"].get_height() // 2 - 1), "player", direction, "proj1", self.screen)
        shot.damage = self.stats["damage"]
        shot.speed = self.stats["shot_speed"]
        shot.inherited = (self.frame_movement[0] * 0.5,
                          self.frame_movement[1] * 0.5)
        for item in self.items:
            item.on_shoot(self, shot)
        room.shots.append(shot)

    
        

    def draw(self):
        if self.dying:
            self.screen.blit(self.death_assets[self.death_frame], self.pos)
        else:
            if self.movement[0]:
                self.screen.blit(self.sprites["up"], self.pos)
            elif self.movement[1]:
                self.screen.blit(self.sprites["right"], self.pos)
            elif self.movement[3]:
                self.screen.blit(self.sprites["left"], self.pos)
            else:
                self.screen.blit(self.sprites["default"], self.pos)

    def bottom(self):
        return self.pos[1] + self.sprites["default"].get_height()

    def hitbox(self):
        return pygame.Rect(self.pos[0] + 2, self.pos[1] + 4, self.sprites["default"].get_width() - 4, self.sprites["default"].get_height() - 5)


    
