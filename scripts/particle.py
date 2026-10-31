from scripts.helpers import *

class Particle:
    def __init__(self, game, p_type, pos, velocity = [0, 0], frame = 0, animation_rate = 2):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = velocity
        self.animation = Animation(load_images(f"particles/{p_type}"), animation_rate, False)
        self.animation.frame = frame

    def update(self):

        kill = False
        if self.animation.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill

    def render(self, screen):
        img = self.animation.img()
        screen.blit(img, (self.pos[0], self.pos[1]))