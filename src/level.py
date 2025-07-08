import pygame
from settings import BLUE

class Level:
    def __init__(self):
        self.platforms = [
            pygame.Rect(100, 500, 600, 40),
            pygame.Rect(300, 400, 200, 20),
        ]

    def draw(self, surface):
        for plat in self.platforms:
            pygame.draw.rect(surface, BLUE, plat) 