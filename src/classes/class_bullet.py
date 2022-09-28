import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_SPEED, key_pressed


class Bullet(pygame.sprite.Sprite):
    BULLED_SCALE = 1

    def __init__(self, pic, x, y, direction, speed=6, falling_without_trajectory=False):
        pygame.sprite.Sprite.__init__(self)
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5][:-4]
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = direction
        self.speed = speed
        self.falling_without_trajectory = falling_without_trajectory

    def direction_shooting(self):
        # print(self.position)
        pygame.mask.from_surface(self.image)  # create mask image
        self.rect.y += self.BULLED_SCALE
        if self.falling_without_trajectory:
            self.rect.y += self.speed
            self.rect.x -= 1
            if key_pressed(pygame.K_RIGHT):
                self.rect.x -= BG_SPEED
        else:
            if self.direction.x == 1:
                self.rect.x += self.speed
            elif self.direction.x == -1:
                self.image = pygame.image.load('assets/images/bullets/spear_left.png')
                self.rect.x -= self.speed

    def prevent_overflow_bullet_group(self):  # remove old shot from bullets_group if shoot out of screen
        if self.rect.x < -30 or self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def update(self):
        self.direction_shooting()
        self.prevent_overflow_bullet_group()
