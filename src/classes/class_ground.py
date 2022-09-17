import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE


class Ground(pygame.sprite.Sprite):
    def __init__(self, picture='../src/assets/images/ground/gr_1.png', x=0, y=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picture).convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass
        # pygame.mask.from_surface(self.image)


