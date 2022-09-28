import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT_SIZE, BG_SPEED, key_pressed
from src.classes.class_sound import Sound


class Enemy(pygame.sprite.Sprite, Sound):
    def __init__(self, pic='', x=0, y=0, speed=0, noise=False):
        pygame.sprite.Sprite.__init__(self)
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5]
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed
        self.noise = noise

    def movement_enemy_current_pos(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= self.speed + BG_SPEED
        else:
            self.rect.x -= self.speed

    def prevent_overflow_item_group(self):  # remove old enemy from item_group if it out of screen
        if self.rect.x < -30 or self.rect.x > SCREEN_WIDTH:
            self.kill()

    def make_sound(self):
        if self.item_name == 'monkey':
            Sound.monkey_sound(self)

    def update(self):
        self.movement_enemy_current_pos()
        self.prevent_overflow_item_group()
        if self.noise:
            self.make_sound()
            self.noise = False

