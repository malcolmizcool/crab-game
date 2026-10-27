import pygame

def load_image(path):
    image = pygame.image.load("assets/" + path)
    return image