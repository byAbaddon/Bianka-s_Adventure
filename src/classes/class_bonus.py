import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, randrange
from src.classes.class_sound import Sound


class Bonus(pygame.sprite.Sprite, Sound):
    SPEED = 4

    def __init__(self, pic='../src/assets/images/items/bonus/coin_small.png'):
        pygame.sprite.Sprite.__init__(self)
        self.item_name = pic.split('/')[6][:-4]
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = [randrange(20, SCREEN_WIDTH - 50), 120]

    def movement(self):
        self.rect.y += self.SPEED

    def prevent_overflow_item_group(self):  # remove old  item if out of screen
        if self.rect.y > SCREEN_HEIGHT - 40:
            self.kill()
            if self.item_name == 'coin_small':
                Sound.coin_fail_in_water(self)
            elif self.item_name == 'star_small':
                Sound.star_fail_out(self)

    def update(self):
        self.prevent_overflow_item_group()
        self.movement()
