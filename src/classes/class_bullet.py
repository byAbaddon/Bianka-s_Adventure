import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet(pygame.sprite.Sprite):
    BULLED_SPEED = 6

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.rotation = 0
        self.image = pygame.image.load('assets/images/bullets/spear_90.png')
        self.rect = self.image.get_rect(center=pos)
        self.position = pos
        self.direction = 1

    def update(self):
        pygame.mask.from_surface(self.image)  # create mask image
        # self.position += self.direction  # Update the position vector.
        self.rect.center = self.position  # Update the position rect.

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT:
            self.kill()  # remove old shot from bullets_group
