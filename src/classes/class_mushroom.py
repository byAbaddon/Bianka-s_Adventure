import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, picture='../src/assets/images/bullets/axe_32.png', x=400,
                 y=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - 32):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../src/assets/images/mushroom/purple.png').convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.image_height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass
        # pygame.mask.from_surface(self.image)