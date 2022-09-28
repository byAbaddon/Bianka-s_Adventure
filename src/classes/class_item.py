import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE, key_pressed, BG_SPEED, BG_LOOP_SPEED_INCREASE


class Item(pygame.sprite.Sprite):
    def __init__(self, pic='', x=SCREEN_WIDTH,  y=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE):
        pygame.sprite.Sprite.__init__(self, )
        self.x = x
        self.y = y
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5][:-4]
        self.image = pygame.image.load(pic).convert_alpha()
        self.image_height_size = self.image.get_height()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midtop = (x, y - self.image_height_size + 13)

        # print(self.group_name, 'g - i -> ' ,self.item_name )

    def movement(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= BG_SPEED
        if key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_a):  # developer hack speed
            self.rect.x -= BG_SPEED + BG_LOOP_SPEED_INCREASE

    def prevent_overflow_item_group(self):  # remove old item from item_group if it out of screen
        if self.rect.x < -80 or self.rect.x > SCREEN_WIDTH:
            self.kill()

    def update(self):
        pygame.mask.from_surface(self.image)
        self.movement()
        self.prevent_overflow_item_group()
