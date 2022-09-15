import pygame
from src.settings import SCREEN_WIDTH, vec


class Bullet(pygame.sprite.Sprite):
    BULLED_SPEED = 6

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/bullets/spear_90.png')
        self.rect = self.image.get_rect()
        self.pos = vec(self.rect.x, self.rect.y)
        self.direction = direction

    def direction_shooting(self):
        # print(self.position)
        pygame.mask.from_surface(self.image)  # create mask image
        # self.position += self.direction  # Update the position vector.
        # self.rect.center = self.position  # Update the position rect.
        if self.direction.x == 1:
            self.rect.x += self.BULLED_SPEED
        elif self.direction.x == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x -= self.BULLED_SPEED

    def update(self):
        self.direction_shooting()

        # remove old shot from bullets_group
        if self.rect.x < -30 or self.rect.x > SCREEN_WIDTH:
            self.kill()
