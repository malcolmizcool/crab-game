import pygame

class Floor:
    def __init__(self):
        pass


class Room:
    def __init__(self):
        self.enemies = []
        self.shots = []
        self.pickups = []
        self.cleared = False
        self.visited = False
        self.doors = {}


    def spawn_enemies(self):
        pass