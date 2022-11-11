import pygame.image

from src.settings import *
from src.classes.class_sound import Sound
from src.classes.class_player import Player


class Enemy(Player, Sound):
    SPRITE_ANIMATION_SPEED = 0.1
    COOLDOWN = 2000
    start_time = pygame.time.get_ticks()

    def __init__(self, class_bullet, all_sprite_groups_dict, background, pic='', x=SCREEN_WIDTH, y=0, speed=0,
                 noise=False, shooting=False, pic_bullet='', bullet_speed=1, sprite_pic_num=0, is_static=False):
        Player.__init__(self, class_bullet, all_sprite_groups_dict)
        self.background = background
        self.group_name = pic.split('/')[4]
        self.item_name = pic.split('/')[5]
        self.image = pygame.image.load(pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = vec(0, -1)  # fall down
        self.speed = speed
        self.noise = noise
        self.shooting = shooting
        self.pic_bullet = pic_bullet
        self.bullet_speed = bullet_speed
        self.current_sprite = 0
        self.sprite_pic_num = sprite_pic_num
        self.sprites_animate = [pygame.image.load(f'{pic[:-5]}{x}.png') for x in range(1, self.sprite_pic_num + 1)]
        self.is_static = is_static
        self.half_position = False
        self.is_visited = False

    def movement_enemy_current_pos(self):
        # ------  standard enemies movement --------
        if key_pressed(pygame.K_RIGHT):
            if not self.is_static:
                self.rect.x -= self.speed + BG_SPEED
            else:
                self.rect.x += self.background.distance_mt - BG_SPEED  # set static enemies Y position
        else:
            if not self.is_static:
                self.rect.x -= self.speed
        # ------  special enemies movement --------
        # print(self.item_name)
        if self.item_name == 'fish':
            self.fish_action()
        if self.item_name == 'octopus':
            self.octopus_action()
        if self.item_name == 'fireball':
            self.fireball_action()
        if self.item_name == 'ghost':
            self.ghost_action()
        if self.item_name == 'eagle_attack':
            self.eagle_attack_action()
        if self.item_name == 'bat_attack':
            self.bat_attack_action()
        if self.item_name == 'vamp':
            self.vamp_action()
        if self.item_name == 'crab':
            self.crab_action()

    def make_sound(self):
        if self.noise:
            if self.item_name in ['monkey', 'raven', 'turtle', 'boar', 'bee', 'mouse', 'mole', 'crab', 'fish', 'ghost',
                                  'octopus', 'dragon', 'vulture', 'turtle', 'monster', 'fireball', 'cockroach',
                                  'penguin', 'seal', 'snowmen', 'eagle', 'eagle_attack', 'bird', 'camel', 'emu', 'elf',
                                  'medusa', 'medusa_attack', 'tiger', 'stone_ball', 'dragon_big', 'dragon_big_attack',
                                  'lizard', 'bat', 'bat_attack', 'vamp', 'knight_sword', 'knight_pike', 'knight_axe',
                                  'crocodile']:
                self.noise = False
                return eval(f'Sound.{self.item_name}_sound(self)')

    def crab_action(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.start_time > self.COOLDOWN:
            Sound.crab_sound(self)
            self.start_time = time_now
            if not self.is_visited:
                self.is_visited = True
            else:
                self.is_visited = False

        if not self.is_visited:
            self.rect.x += 1
        else:
            self.rect.x -= 1

    def eagle_attack_action(self):
        if self.rect.x <= SCREEN_WIDTH - 100:
            self.sprite_pic_num = 0
            self.image = pygame.image.load('../src/assets/images/enemies/eagle/11.png')
            self.rect.y += self.speed

    def bat_attack_action(self):
        if self.rect.x <= SCREEN_WIDTH - 200:
            self.sprite_pic_num = 0
            self.image = pygame.image.load('../src/assets/images/enemies/bat_attack/5.png')
            self.rect.y += self.speed

    def ghost_action(self):
        if self.rect.x <= SCREEN_WIDTH - 100:
            self.rect.y += 2

    def fireball_action(self):
        if not self.is_visited:
            Sound.thunder_sound(self)
            self.rect.x = randrange(SCREEN_WIDTH // 2, SCREEN_WIDTH)
            self.is_visited = True
        self.rect.y += self.speed

    def vamp_action(self):
        if not self.is_visited:
            Sound.thunder_sound(self)
            self.rect.x = randrange(SCREEN_WIDTH // 3, SCREEN_WIDTH)
            self.is_visited = True
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT - GROUND_HEIGHT_SIZE :
            self.image = pygame.image.load('../src/assets/images/enemies/vamp/2.png')

    def octopus_action(self):
        if not self.is_visited:
            self.rect.x = SCREEN_WIDTH
            self.is_visited = True
        if self.rect.y > 120 and not self.half_position:
            self.rect.y -= self.speed
            self.image = pygame.image.load('../src/assets/images/enemies/octopus/1.png').convert_alpha()
        else:
            self.half_position = True
            self.rect.y += self.speed
            self.image = pygame.image.load('../src/assets/images/enemies/octopus/2.png').convert_alpha()
            if self.rect.y > SCREEN_HEIGHT:
                self.half_position = False

    def fish_action(self):
        if not self.half_position and self.rect.y > 300:  # go to up pos
            self.rect.x -= self.speed
            self.rect.y -= 1
            if self.rect.y == 300:
                self.image = pygame.transform.rotate(self.image, + 15)
        elif self.half_position and self.rect.x > 570:  # middle pos
            self.rect.x -= 1
        else:  # go to down pos
            self.half_position = True
            self.rect.y += 1
            self.rect.x -= self.speed + 1

    def sprite_frames(self):
        if self.sprite_pic_num > 0:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED  # speed may be changed
            if self.current_sprite >= len(self.sprites_animate):
                self.current_sprite = 1
            self.image = self.sprites_animate[int(self.current_sprite)]

    def shooting_enemy(self):  # shooting:
        if self.shooting:
            # Add bullet name enemy to class bullet !!!
            if self.item_name in ['snowmen', 'camel', 'dragon_big_attack', 'medusa_attack']:   # enemies with shooting only left
                Sound.bullet_fail(self)
                shot_position = self.rect.midright
                self.direction = vec(-1, 0)
                x = shot_position[0] - self.image.get_width() - 10
                y = SCREEN_HEIGHT - self.image.get_height()
                bullet = self.class_bullet(self.pic_bullet, x, y, self.direction, self.bullet_speed, False)
                self.all_sprite_groups_dict['bullets'].add(bullet)
                self.shooting = False
            elif self.rect.x <= SCREEN_WIDTH - 100:  # enemies shooting down + left
                Sound.bullet_fail(self)
                shot_position = self.rect.midbottom
                x = shot_position[0] + self.image.get_width() // 4 - 30
                y = shot_position[1] + 10  # get y pos form rect
                bullet = self.class_bullet(self.pic_bullet, x, y, self.direction, self.bullet_speed, True)
                self.all_sprite_groups_dict['bullets'].add(bullet)
                self.shooting = False

    def prevent_overflow_item_group(self):  # remove old enemy from item_group if it out of screen
        if self.rect.x < -200 or self.rect.x > SCREEN_WIDTH + 100 or self.rect.y > SCREEN_HEIGHT + 100:
            self.kill()

    def update(self):
        self.sprite_frames()
        self.movement_enemy_current_pos()
        self.make_sound()
        self.shooting_enemy()
        self.prevent_overflow_item_group()



