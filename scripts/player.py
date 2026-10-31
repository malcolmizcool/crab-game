import pygame
from scripts.helpers import *
from scripts.projectiles import *
from scripts.entities import *
from  scripts.item_script import *

SHOOT_DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_RIGHT: (1, 0),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
}

class Player(Entity):
    def __init__(self, game, screen, scene):
        super().__init__([SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2], game, screen, {
            "default": Animation([load_image("player/char_default.png")]),
            "left": Animation([load_image("player/char_left.png")]),
            "right":   Animation([load_image("player/char_right.png")]),
            "up":      Animation([load_image("player/char_up.png")]),
            "death":   Animation(load_images("player/char_death"), img_dur=ANIMATION_SPEED, loop=False),
        })

        self.scene = scene

        self.items = []
        self.hitbox_offset = (2, 4, 2, 1)
        self.stats = {
            "velocity": [0, 0],
            "speed": 1,
            "damage": 3,
            "fire_rate": 30,
            "shot_speed": 1,
            "range": 45,
            "coins": 0,
        }
        self.health = 6
        self.invincibility_time = 60
        self.movement = [False, False, False, False]


        self.shot_cooldown = 0



    def on_death_finished(self):
        self.game.screenState = "gameover"





    def update(self, events, room):
        super().update(room)
        if self.dying:
            return      # no moving or shooting during the death animation

#----------------------------------------------------------
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
        self.move(self.frame_movement[0], self.frame_movement[1], room)
        if self.movement[0]:
            self.facing = "up"
        elif self.movement[1]:
            self.facing = "right"
        elif self.movement[3]:
            self.facing = "left"
        else:
            self.facing = "default"
# other projectiles

        for shot in room.shots:
            if shot.owner == "player" or shot.dying or not shot.alive:
                continue 
            shot_rect = shot.hitbox()
            player_rect = self.hitbox()

            if player_rect.colliderect(shot_rect):
                if any(item.on_hit(self, shot) for item in self.items):
                    continue        # an item dealt with it (e.g. Rebound), so no damage
                self.take_damage(shot.damage)
                shot.kill()

# items 
        for pickup in room.pickups:
            if pickup.alive and self.hitbox().colliderect(pickup.hitbox()):
                pickup.collect(self)
        room.pickups = [p for p in room.pickups if p.alive]



#--------------------------------------------------------------------------
#other
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                room.spawn_enemies()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                room.add_pickup(ItemPickup("receipt", (SCREEN_WIDTH  // 2, SCREEN_HEIGHT // 2), self.game, self.screen))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                self.scene.chat.send("hello, world!")

                


#---------------------------------------------------------------------------

    def shoot(self, direction, room):
        shot = Shot(self.center(), "player", direction, "proj1", self.screen)
        shot.damage = self.stats["damage"]
        shot.speed = self.stats["shot_speed"]
        shot.range = self.stats["range"]
        shot.inherited = (self.frame_movement[0] * 0.5,
                          self.frame_movement[1] * 0.5)
        for item in self.items:
            item.on_shoot(self, shot)
        room.shots.append(shot)

    def add_item(self, item):
        self.items.append(item)
        item.on_pickup(self)






    
