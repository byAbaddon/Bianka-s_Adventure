import pygame
from src.settings import SCREEN_HEIGHT, GROUND_HEIGHT_SIZE, key_pressed, BG_SPEED


class Ground(pygame.sprite.Sprite):
    def __init__(self, pic='../src/assets/images/ground/gr_1.png', is_static=True, x=0, y=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE + 10):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.x = x
        self.rect.y = y
        self.is_static = is_static

    def movement(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= BG_SPEED

    def update(self):
        if not self.is_static:
            self.movement()



