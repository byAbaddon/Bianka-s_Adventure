import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE, key_pressed, BG_SPEED, BG_LOOP_SPEED_INCREASE


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, picture='../src/assets/images/', x=SCREEN_WIDTH, y=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - 4):
        pygame.sprite.Sprite.__init__(self,)
        self.image = pygame.image.load(picture).convert_alpha()
        self.image_height = self.image.get_height()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (x, y)

    def movie(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= BG_SPEED
        if key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_a):
            self.rect.x -= BG_SPEED + BG_LOOP_SPEED_INCREASE

    def update(self):
        pygame.mask.from_surface(self.image)
        self.movie()
