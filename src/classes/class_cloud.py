import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, vec, key_pressed, BG_SPEED
from src.classes.class_player import Player


class Cloud(Player):

    def __init__(self, class_bullet, all_sprite_groups_dict, pic='../src/assets/images/cloud/static.png',
                 x=SCREEN_WIDTH, y=0, is_static=True, speed=0, direction=(1, 1), distance=20):
        Player.__init__(self, class_bullet, all_sprite_groups_dict)
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5]
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed
        self.is_static = is_static
        self.direction = vec(direction)  # vec(0, -1)  # fall down
        self.distance = distance
        self.distance_counter = 0
        self.is_distance_done = False

    def movement_could_in_screen_if_key_preset(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= self.speed + BG_SPEED
        else:
            self.rect.x -= self.speed

    def movement_could_left_right(self):
        if self.distance_counter < self.distance and not self.is_distance_done:  # left
            self.rect.x -= 1
            self.distance_counter += 1
            if self.distance_counter == self.distance:
                self.is_distance_done = True
        if self.is_distance_done:  # right
            if self.distance_counter > 0:
                self.rect.x += 1
                self.distance_counter -= 1
                self.is_distance_done = False

    def movement_could_up_down(self):
        if self.distance_counter < self.distance and not self.is_distance_done:  # left
            self.rect.y -= 1
            self.distance_counter += 1
            if self.distance_counter == self.distance:
                self.is_distance_done = True
        if self.is_distance_done:  # right
            if self.distance_counter > 0:
                self.rect.y += 1
                self.distance_counter -= 1
                self.is_distance_done = False

    def prevent_overflow_item_group(self):  # remove old enemy from item_group if it out of screen
        if self.rect.x < -60 or self.rect.x > SCREEN_WIDTH + 100:
            self.kill()

    def update(self):
        self.movement_could_in_screen_if_key_preset()
        self.prevent_overflow_item_group()
        if not self.is_static:
            if self.direction == (-1 or 1):
                self.movement_could_left_right()
            else:
                self.movement_could_up_down()


