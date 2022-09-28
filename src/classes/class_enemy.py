import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT_SIZE, BG_SPEED, TOP_FRAME_SIZE, key_pressed
from src.classes.class_sound import Sound


class Enemy(pygame.sprite.Sprite, Sound):
    SPRITE_ANIMATION_SPEED = 0.1

    def __init__(self, pic='', x=0, y=0, speed=0, noise=False, sprite_pic_num=0):
        pygame.sprite.Sprite.__init__(self)
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5]
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed
        self.noise = noise
        self.current_sprite = 0
        self.sprite_pic_num = sprite_pic_num
        self.sprites_animate = [pygame.image.load(f'{pic[:-5]}{x}.png') for x in range(1, self.sprite_pic_num + 1)]

        # src/assets/images/enemies/raven
    def movement_enemy_current_pos(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= self.speed + BG_SPEED
        else:
            self.rect.x -= self.speed

    def sprite_frames(self):
        if self.sprite_pic_num > 0:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED  # speed may be changed
            if self.current_sprite >= len(self.sprites_animate):
                self.current_sprite = 1
            self.image = self.sprites_animate[int(self.current_sprite)]

    def prevent_overflow_item_group(self):  # remove old enemy from item_group if it out of screen
        if self.rect.x < -30 or self.rect.x > SCREEN_WIDTH:
            self.kill()

    def make_sound(self):
        if self.noise:
            if self.item_name == 'monkey':
                Sound.monkey_sound(self)
            elif self.item_name == 'raven':
                Sound.raven_sound(self)
        self.noise = False

    def update(self):
        self.movement_enemy_current_pos()
        self.sprite_frames()
        self.prevent_overflow_item_group()
        self.make_sound()


# ---------------------------------------------------------------------- create Enemies


# variables
pic_monkey = '../src/assets/images/enemies/monkey/monkey.png'
pic_hedgehog = '../src/assets/images/enemies/hedgehog/hedgehog.png'
pic_raven = '../src/assets/images/enemies/raven/1.png'
# create enemy classes
enemy_monkey = Enemy(pic_monkey, SCREEN_WIDTH, 150, 5, True)

enemy_hedgehog = Enemy(pic_hedgehog, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - 5, 1)
enemy_static_hedgehog = Enemy(pic_hedgehog, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - 5, 0)

enemy_raven = Enemy(pic_raven, SCREEN_WIDTH, TOP_FRAME_SIZE + 100, 3, True, 5)

enemy_classes_dict = {'enemy_monkey': enemy_monkey, 'enemy_hedgehog': enemy_hedgehog, 'enemy_raven': enemy_raven,
                      'enemy_static_hedgehog': enemy_static_hedgehog}
