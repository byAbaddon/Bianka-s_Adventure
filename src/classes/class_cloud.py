import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, key_pressed, BG_SPEED, vec


class Cloud(pygame.sprite.Sprite):
    def __init__(self, player_data, background_data, pic='../src/assets/images/cloud/static.png',
                 x=SCREEN_WIDTH, y=SCREEN_HEIGHT - 350, is_static=True, speed=int(1), direction='left_right or up_down',
                 distance=100):
        pygame.sprite.Sprite.__init__(self,)
        self.player_data = player_data
        self.background_data = background_data
        self.direction = direction
        self.group_name = pic.split('/')[4]
        self.item_name = self.direction
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed_cloud = int(speed)
        self.is_static = is_static
        self.current_direction = vec(0, 0)
        self.distance = distance
        self.distance_counter = distance
        self.is_distance_done = False
        self.is_firs_hit = False
        self.is_player_and_cloud_collide = False
        self.is_background_fixed_if_player_on_platform = True

    def movement_could_in_screen_if_key_preset(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= BG_SPEED

    def movement_could_left_right(self):
        if not self.is_distance_done:  # left
            self.current_direction.x = -1
            self.rect.x -= self.speed_cloud
            self.distance_counter -= self.speed_cloud
            if self.distance_counter == 0:
                self.is_distance_done = True
        if self.is_distance_done:  # right
            self.current_direction.x = 1
            if self.distance_counter < self.distance:
                self.rect.x += self.speed_cloud
                self.distance_counter += self.speed_cloud
                if self.distance_counter == self.distance:
                    self.is_distance_done = False
        # balance if could movie left / right
        if self.is_player_and_cloud_collide:
            if self.current_direction.x == 1:
                self.player_data.pos.x += self.speed_cloud
            if self.current_direction.x == -1:
                self.player_data.pos.x -= self.speed_cloud
            elif key_pressed(pygame.K_RIGHT) or key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_UP):
                self.player_data.direction.x = 1
            self.is_player_and_cloud_collide = False

    def movement_could_up_down(self):
        if not self.is_distance_done:  # up
            self.current_direction.y = -1
            self.rect.y -= self.speed_cloud
            self.distance_counter -= self.speed_cloud
            if self.distance_counter == 0:
                self.is_distance_done = True
        if self.is_distance_done:  # down
            self.current_direction.y = +1
            if self.distance_counter < self.distance:
                self.rect.y += self.speed_cloud
                self.distance_counter += self.speed_cloud
                if self.distance_counter == self.distance:
                    self.is_distance_done = False

    def movement_could_fail(self):
        if self.is_player_and_cloud_collide:
            self.rect.y += self.speed_cloud + 2

    def check_collide(self):
        group_items = self.player_data.all_sprite_groups_dict['items']
        for sprite in pygame.sprite.spritecollide(self.player_data,  group_items,  False, pygame.sprite.collide_mask):
            if sprite.group_name == 'cloud':
                if self.player_data.pos.y < sprite.rect.bottom:
                    # # ------------------------------fix position after jump right on cloud
                    if not self.is_firs_hit:
                        self.player_data.direction = vec(1, 1)
                        self.is_firs_hit = True
                    if key_pressed(pygame.K_RIGHT) or key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_UP):
                        self.player_data.direction = vec(1, 1)
                    # ------------------------------------
                    if sprite.item_name == 'left_right' or sprite.item_name == 'fail':
                        self.is_player_and_cloud_collide = True
                    # todo  fix bg if player on the could
                    # if sprite.item_name == 'left_right' and self.is_background_fixed_if_player_on_platform:
                    #     print( self.player_data.pos.x , ' x   bor  ',  self.player_data.WALK_RIGHT_SCREEN_BORDER)
                    #     if self.player_data.pos.x > self.player_data.WALK_RIGHT_SCREEN_BORDER:
                    #         self.background_data.bg_counter -= self.speed_cloud
                        # else:
                        #     self.is_background_fixed_if_player_on_platform = False

    def prevent_overflow_item_group(self):  # remove old item from item_group if it out of screen
        if self.rect.x < -200 or self.rect.x > SCREEN_WIDTH + 100 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def update(self):
        self.movement_could_in_screen_if_key_preset()
        self.prevent_overflow_item_group()
        if not self.is_static:
            self.check_collide()
            if self.direction == 'left_right':  # left/right
                self.movement_could_left_right()
            elif self.direction == 'up_down':  # up/down
                self.movement_could_up_down()
            elif self.direction == 'fail':  # fail:
                self.movement_could_fail()



