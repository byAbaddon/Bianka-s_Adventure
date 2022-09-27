import pygame
from src.settings import SCREEN_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pic='../src/assets/images/enemies/monkey/monkey.png', x=0, y=0, speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5]
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed

    def movement(self):
        self.rect.x -= self.speed

    def prevent_overflow_item_group(self):  # remove old enemy from item_group if it out of screen
        if self.rect.x < -30 or self.rect.x > SCREEN_WIDTH:
            self.kill()

    def update(self):
        self.movement()
        self.prevent_overflow_item_group()

