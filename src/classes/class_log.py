import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT_SIZE, key_pressed, BG_SPEED, vec


class Log(pygame.sprite.Sprite):
    def __init__(self, player_data, pic='../src/assets/images/cloud/static.png', x=SCREEN_WIDTH,
                 y=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE, is_static=True, speed=1, direction='left_right or up_down', distance=100):
        pygame.sprite.Sprite.__init__(self,)
        self.player_data = player_data
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5]
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed
        self.is_static = is_static
        self.direction = direction
        self.current_direction = vec(0, 0)
        self.distance = distance
        self.distance_counter = distance
        self.is_distance_done = False

    def movement_log_in_screen_if_key_preset(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= BG_SPEED # todo: fix logs in level and set new
            # self.rect.x -= self.speed + BG_SPEED  # old

    def movement_log_left_right(self):
        if not self.is_distance_done:  # left
            self.current_direction.x = -1
            self.rect.x -= self.speed
            self.distance_counter -= self.speed
            if self.distance_counter == 0:
                self.is_distance_done = True
        if self.is_distance_done:  # right
            self.current_direction.x = 1
            if self.distance_counter < self.distance:
                self.rect.x += self.speed
                self.distance_counter += self.speed
                if self.distance_counter == self.distance:
                    self.is_distance_done = False

    def movement_log_up_down(self):
        if not self.is_distance_done:  # up
            self.current_direction.y = -1
            self.rect.y -= self.speed
            self.distance_counter -= self.speed
            if self.distance_counter == 0:
                self.is_distance_done = True
        if self.is_distance_done:  # down
            self.current_direction.y = +1
            if self.distance_counter < self.distance:
                self.rect.y += self.speed
                self.distance_counter += self.speed
                if self.distance_counter == self.distance:
                    self.is_distance_done = False

    def check_collide(self):
        group_items = self.player_data.all_sprite_groups_dict['items']
        for sprite in pygame.sprite.spritecollide(self.player_data,  group_items,  False, pygame.sprite.collide_mask):
            if sprite.group_name == 'logs' or 'stone':
                if self.current_direction.x == 1:
                    self.player_data.pos.x += self.speed
                if self.current_direction.x == -1:
                    self.player_data.pos.x -= self.speed

    def prevent_overflow_item_group(self):  # remove old item from item_group if it out of screen
        if self.rect.x < -200 or self.rect.x > SCREEN_WIDTH + 100:
            self.kill()

    def update(self):
        self.movement_log_in_screen_if_key_preset()
        self.prevent_overflow_item_group()
        if not self.is_static:
            if self.direction == 'left_right':  # left/right
                self.movement_log_left_right()
                self.check_collide()
            else:
                self.movement_log_up_down()


