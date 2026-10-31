import pygame

from scripts.helpers import *
from data.constants import *

class GameOver:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.asset = load_image("misc/death_overlay.png")
        self.title_text = pygame.Font("assets/fonts/PixeloidSans.ttf", 10)

    def run(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game.new_game()

        self.draw()

    def draw(self):
        self.screen.blit(self.asset, (SCREEN_WIDTH // 2 - self.asset.get_width() // 2, SCREEN_HEIGHT // 2 - self.asset.get_height() // 2))
        game_over = self.title_text.render("Game over!", False, (255, 255, 255))
        self.screen.blit(game_over, (SCREEN_WIDTH // 2 - self.asset.get_width() // 2 + 25, SCREEN_HEIGHT // 2 - self.asset.get_height() // 2 + game_over.get_height() // 2))