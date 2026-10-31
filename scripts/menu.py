import pygame
from data.constants import *


def arrange_buttons(buttons, game):
        width = SCREEN_WIDTH // 4
        height = SCREEN_HEIGHT // 12
        gap = SCREEN_HEIGHT // 30
        start_x = SCREEN_WIDTH // 2 - width // 2
        start_y = SCREEN_HEIGHT // 2 - (len(buttons) * (height + gap)) // 2

        arranged_buttons = []
        for i, (text, action) in enumerate(buttons):
            y = start_y + i * (height + gap)
            arranged_buttons.append(
                game.button((start_x, y), (width, height), text, game.font, (0, 0, 0), game.screen, game, action)
            )

        return arranged_buttons



class Menu:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

        self.menuState = "home" #shows the save files. when a file is selected, start game and load the save file
        self.titletext = self.game.font.render("super cool crab game!", True, (255, 255, 255))


        # --- buttons ---

        button_labels_and_actions = [
            ("new game", self.new_game),
            ("continue", self.start_game),
            ("settings", self.open_settings),
            ("editor", self.open_level_editor)
        ]

        self.buttons = arrange_buttons(button_labels_and_actions, game)

        self.test_image = pygame.image.load("assets/entities/King_Blob.png").convert_alpha()

    def open_settings(self):
        self.game.change_screen_state("settings")

    def open_level_editor(self):
        try:
            with open("level.json", "r") as f:
                pass
        except:
            pass
        self.game.change_screen_state("editor")

    def new_game(self):
        self.game.new_game()

    def start_game(self):
        self.game.change_screen_state("game")

    def gui(self, events):
        
        if self.menuState == "home":
            for button in self.buttons:
                button.update(events, self.game.mouse_pos())

    def run(self, events):

        self.screen.fill((0, 0, 0)) 
    


        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print("settings clicked!")
                    self.game.screenState = "settings"

        
        

        self.screen.blit(self.titletext, (SCREEN_WIDTH // 2 - self.titletext.get_width() // 2, 20))
        self.screen.blit(self.test_image, (SCREEN_WIDTH // 2 - self.test_image.get_width() // 2, 110))
        self.gui(events)

class PauseMenu:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

        button_labels_and_actions = [
            ("resume", self.resume_game),
            ("settings", self.open_settings),
            ("quit", self.quit_to_menu)
        ]

        self.buttons = arrange_buttons(button_labels_and_actions, game)


    def resume_game(self):
        self.game.change_screen_state("game")

    def open_settings(self):
        self.game.change_screen_state("settings")

    def quit_to_menu(self):
        self.game.change_screen_state("menu")

    def gui(self, events):
        for button in self.buttons:
            button.update(events, self.game.mouse_pos())