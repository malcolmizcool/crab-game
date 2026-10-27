import pygame
import os

def load_image(path):
    image = pygame.image.load("assets/" + path)
    return image

def load_images(path):
    images = []
    for img_name in  os.listdir("assets/" + path):
        images.append(load_image(path + '/' + img_name))

    return images