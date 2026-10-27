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
    def __init__(self, game, screen, debugState):
        self.pos = [50, 50]
        self.items = []
        self.game = game
        self.screen = screen
        self.debugState = debugState
        self.stats = {
            "health": 6,
            "velocity": [0, 0],
            "damage": 3,
            "fire_rate": 30,
            "coins": 0,
        }
        self.movement = [False, False, False, False]
        self.sprites = {"right": load_image("player/char_right.png"),
                        "left": load_image("player/char_left.png"),
                        "up": load_image("player/char_up.png"),
                        "default": load_image("player/char_default.png")}

        self.shot_cooldown = 0

        self.player_projectiles = []



    def update(self, events):
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
        frame_movement = (x_input + self.stats["velocity"][0],
                          y_input + self.stats["velocity"][1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
#---------------------------------------------------------------------------------

        if self.shot_cooldown > 0:                              #shot logic etc etc
            self.shot_cooldown -= 1

        keys = pygame.key.get_pressed()
        for key, direction in SHOOT_DIRECTIONS.items():
            if keys[key] and self.shot_cooldown == 0:
                self.shoot(direction)
                self.shot_cooldown = self.stats["fire_rate"]
                break
                


        for shot in self.player_projectiles:
            shot.update()


#--------------------------------------------------------------------------------------
        self.draw()                                            #drawing

    def shoot(self, direction):
        shot = Shot((self.pos[0] + self.sprites["right"].get_width() // 2 - 2, self.pos[1] + self.sprites["right"].get_height() // 2 - 1), direction, self.screen)
        for item in self.items:
            item.on_shoot(self, shot)
        self.player_projectiles.append(shot)
        

    def draw(self):
        if self.movement[0]:
            self.screen.blit(self.sprites["up"], self.pos)
        elif self.movement[1]:
            self.screen.blit(self.sprites["right"], self.pos)
        elif self.movement[3]:
            self.screen.blit(self.sprites["left"], self.pos)
        else:
            self.screen.blit(self.sprites["default"], self.pos)
            


    
