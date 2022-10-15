from src.settings import *
from src.classes.class_sound import Sound
from src.classes.class_player import Player


class Enemy(Player, Sound):
    SPRITE_ANIMATION_SPEED = 0.1

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
        if self.item_name == 'fish':
            self.fish_action()
        if self.item_name == 'octopus':
            self.octopus_action()
        if self.item_name == 'fireball':
            self.fireball_action()

    def fireball_action(self):
        if not self.is_visited:
            Sound.thunder_sound(self)
            self.rect.x = randrange(SCREEN_WIDTH // 2, SCREEN_WIDTH)
            self.is_visited = True
        self.rect.y += self.speed

    def octopus_action(self):
        if not self.is_visited:
            self.rect.x = SCREEN_WIDTH // 2
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
        else: # go to down pos
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
            if self.rect.x <= SCREEN_WIDTH - 100:
                Sound.bullet_fail(self)
                shot_position = self.rect.midbottom
                x = shot_position[0] + self.image.get_width() // 4 - 30
                y = shot_position[1] - 15  # get y pos form rect
                bullet = self.class_bullet(self.pic_bullet, x, y, self.direction, self.bullet_speed, True)
                self.all_sprite_groups_dict['bullets'].add(bullet)
                self.shooting = False

    def prevent_overflow_item_group(self):  # remove old enemy from item_group if it out of screen
        if self.rect.x < -200 or self.rect.x > SCREEN_WIDTH + 100 or self.rect.y > SCREEN_HEIGHT + 100:
            self.kill()

    def make_sound(self):
        if self.noise:
            if self.item_name in ['monkey', 'raven', 'turtle', 'boar', 'bee', 'mouse', 'mole', 'crab', 'fish',
                                  'octopus', 'dragon', 'vulture', 'turtle', 'monster', 'fireball', 'cockroach']:
                self.noise = False
                return eval(f'Sound.{self.item_name}_sound(self)')

    def update(self):
        self.sprite_frames()
        self.movement_enemy_current_pos()
        self.make_sound()
        self.shooting_enemy()
        self.prevent_overflow_item_group()



