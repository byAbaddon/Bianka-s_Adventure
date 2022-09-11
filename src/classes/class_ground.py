import pygame
from src.settings import SCREEN_HEIGHT


class Ground(pygame.sprite.Sprite):
    def __init__(self, picture='../src/assets/images/ground/gr_1.png',  x=0, y=SCREEN_HEIGHT - 78):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picture).convert()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.x = x
        self.rect.y = y



