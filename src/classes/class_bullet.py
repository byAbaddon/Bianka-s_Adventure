import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT_SIZE, BG_SPEED, key_pressed


class Bullet(pygame.sprite.Sprite):
    BULLED_SCALE = 1

    def __init__(self, pic, x, y, direction, speed=6, falling_without_trajectory=False, ):
        pygame.sprite.Sprite.__init__(self)
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5][:-4]
        self.pic = pic
        self.image = pygame.image.load(self.pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = direction
        self.speed = speed
        self.falling_without_trajectory = falling_without_trajectory

    def weapon_capability(self):
        if self.item_name == 'knife':
            self.BULLED_SCALE = 2
            self.speed = 7
        if self.item_name == 'spear':
            self.BULLED_SCALE = 1
            self.speed = 6
        if self.item_name == 'axe':
            self.BULLED_SCALE = 2
            self.speed = 5

    def direction_shooting(self):

        pygame.mask.from_surface(self.image)  # create mask image
        self.rect.y += self.BULLED_SCALE
        if self.falling_without_trajectory:
            self.rect.y += self.speed
            self.rect.x -= 1
            if key_pressed(pygame.K_RIGHT):
                self.rect.x -= BG_SPEED
        else:
            if self.direction.x == 1:
                self.rect.x += self.speed
            elif self.direction.x == -1:
                if self.item_name in ['snowball', 'spit']:  # ----- shooting  left
                    self.rect.x -= self.speed
                    self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - self.image.get_height() - 25
                    if self.item_name == 'spit':
                        self.rect.y -= 35
                    if key_pressed(pygame.K_RIGHT):  # if player movie right fix bullet position
                        self.rect.x -= BG_SPEED
                else:  # ---------------------------------- shooting down + right
                    flipped_image = pygame.image.load(self.pic)
                    self.image = pygame.transform.flip(flipped_image, True, False)
                    self.rect.x -= self.speed

    def prevent_overflow_bullet_group(self):  # remove old shot from bullets_group if shoot out of screen
        if self.rect.x < -30 or self.rect.x > SCREEN_WIDTH + 100 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def update(self):
        self.direction_shooting()
        self.weapon_capability()
        self.prevent_overflow_bullet_group()
