import pygame
from data.constants import *

CHAT_BUFFER = 3
TEXT_COLOUR = (255, 255, 255)
CHAT_TIME = 180
NUMBER_OF_CHATS_SHOWN = 4


class ChatLog:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.Font("assets/fonts/PixeloidSans.ttf", 9)


        self.messages = []

    def send(self, text):
        text = str(text)
        self.messages.insert(0, {
            "text": text,                                         
            "image": self.font.render(text, False, TEXT_COLOUR),
            "timer": CHAT_TIME,                                   
        })

    def update(self):
        for message in self.messages[:NUMBER_OF_CHATS_SHOWN]:
            if message["timer"] > 0:
                message["timer"] -= 1

    def draw(self):
        for i, message in enumerate(self.messages[:NUMBER_OF_CHATS_SHOWN]):
            if message["timer"] > 0:
                y = SCREEN_HEIGHT - (i + 1) * (self.font.get_height() + CHAT_BUFFER)
                self.screen.blit(message["image"], (CHAT_BUFFER, y))
