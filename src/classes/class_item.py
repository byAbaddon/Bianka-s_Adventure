import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE, key_pressed, BG_SPEED, BG_LOOP_SPEED_INCREASE
from src.classes.class_sound import Sound


class Item(pygame.sprite.Sprite, Sound):
    def __init__(self, pic='../src/assets/images/signs/start.png', x=SCREEN_WIDTH, y=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE):
        pygame.sprite.Sprite.__init__(self,)
        self.x = x
        self.y = y
        self.group_name = pic.split('/')[-2]
        self.item_name = pic.split('/')[-1][:-4]
        self.image = pygame.image.load(pic).convert_alpha()
        self.image_height_size = self.image.get_height()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midtop = (x, y - self.image_height_size + 13)
        self.is_sound_played = False

    def enemy_current_pos(self, speed=0, y_pos=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE):
        self.rect.y = y_pos
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= speed + BG_SPEED
        else:
            self.rect.x -= speed

    def movie(self):
        if self.group_name != 'enemies':
            if key_pressed(pygame.K_RIGHT):
                self.rect.x -= BG_SPEED
            if key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_a):  # developer hack speed
                self.rect.x -= BG_SPEED + BG_LOOP_SPEED_INCREASE
        else:
            if self.rect.x > -200:  # prevent animation if out of screen
                if self.item_name == 'monkey':
                    self.enemy_current_pos(speed=3, y_pos=90)
                    if not self.is_sound_played:
                        Sound.monkey_sound(self)
                        self.is_sound_played = True
                if self.item_name == 'hedgehog':
                    self.enemy_current_pos(speed=1, y_pos=486)

    def update(self):
        pygame.mask.from_surface(self.image)
        self.movie()
