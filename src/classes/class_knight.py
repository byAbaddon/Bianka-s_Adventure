import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE, vec
from src.classes.class_sound import Sound


class Knight(pygame.sprite.Sprite, Sound,):
    SPRITE_ANIMATION_SPEED = 0.3
    COOLDOWN = 1000  # milliseconds
    COOLDOWN_ATTACK= {'run': 600, 'attack': 800, 'dead': 1000}  # milliseconds
    WALK_LEFT_SCREEN_BORDER = 20  # is knight w_size
    WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH - 20
    WALK_SPEED = 1
    JUMP_HEIGHT = -6
    energy_power = 200
    is_walk = False
    is_run = False
    is_jump = False
    is_attack = False
    is_dead = False

    def __init__(self, class_bullet, all_sprite_groups_dict):
        pygame.sprite.Sprite.__init__(self)
        self.class_bullet = class_bullet
        self.all_sprite_groups_dict = all_sprite_groups_dict
        self.image = pygame.image.load('../src/assets/images/boss_knight/idle/1.png')
        self.sprites_knight = [pygame.image.load(f'../src/assets/images/boss_knight/idle/{x}.png') for x in range(1, 11)]
        self.current_sprite = 0
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midbottom = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE)
        self.direction = vec(0, 1)  # stay/idle 0
        self.pos = vec(self.rect.x, self.rect.y)

    def knight_movie(self):
        # go left
        if self.is_walk and self.pos.x < 200:
            self.pos.x += self.WALK_SPEED

    def sprite_frames(self):
        key = pygame.key.get_pressed()
        # left and right animation
        if self.direction.y == 1:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites_knight):
                self.current_sprite = 1
            self.image = self.sprites_knight[int(self.current_sprite)]

    def check_collide(self):
        pass

    def update(self,):
        self.sprite_frames()
        self.knight_movie()
