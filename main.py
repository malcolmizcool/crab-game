import pygame


from menu import Menu, PauseMenu
from editor import LevelEditor
from data.constants import *

pygame.init()


class Button:
    def __init__(self, pos, size, text, font, text_colour, screen, game, on_click, selected=False):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.font = font
        self.text_colour = text_colour
        self.game = game
        self.screen = screen
        self.text_surface = self.font.render(self.text, True, self.text_colour)
        self.on_click = on_click
        self.selected = selected

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        if self.selected:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)  # Green border for selected button
        
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def update(self, events, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.selected = True
        else:
            self.selected = False
        for event in events:
            if self.selected and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                self.on_click()

                

        self.draw(self.screen)



class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((SCREEN_WIDTH * SCALE, SCREEN_HEIGHT * SCALE)) 
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font("assets/fonts/PixeloidSans.ttf", SCREEN_HEIGHT * 36 // 600)  
        self.button = Button


        self.screenState = "menu" #default screen state. 
        self.debugState = False 

        self.menu = Menu(self, self.screen, self.debugState)
        self.level_editor = LevelEditor(self)
        self.pause = PauseMenu(self, self.screen, self.debugState)


    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events: #quit event
                if event.type == pygame.QUIT:
                    self.running = False



            if self.screenState == "menu": #the following are all the different game states. switch between to change the functionality of the game/screen
                self.menu.run(events)



            elif self.screenState == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.screenState = "pause"
                self.screen.fill((0, 255, 0))

            elif self.screenState == "gameover":
                pass

            elif self.screenState == "settings":
                self.screen.fill((0, 0, 0)) 

            elif self.screenState == "editor":
                self.level_editor.run(events)

            elif self.screenState == "pause":
                self.pause.gui(events)





            pygame.transform.scale(self.screen, self.window.get_size(), self.window)
            pygame.display.flip()
            self.clock.tick(60)

    def change_screen_state(self, new_state):
        self.screenState = new_state

    def mouse_pos(self):
        # the window is SCALE times bigger than self.screen, so convert to game pixels
        x, y = pygame.mouse.get_pos()
        return x // SCALE, y // SCALE





if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()   

