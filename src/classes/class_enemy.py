from src.settings import *
from src.classes.class_sound import Sound
from src.classes.class_player import Player


class Enemy(Player, Sound):
    SPRITE_ANIMATION_SPEED = 0.1

    def __init__(self, class_bullet, all_sprite_groups_dict, pic='', x=SCREEN_WIDTH, y=0, speed=0, noise=False, shooting=False,
                 pic_bullet='', bullet_speed=1, sprite_pic_num=0):
        Player.__init__(self, class_bullet, all_sprite_groups_dict)
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
        self.sprites_animate = None
        self.sprites_animate = [pygame.image.load(f'{pic[:-5]}{x}.png') for x in range(1, self.sprite_pic_num + 1)]

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
        if self.rect.x < -60 or self.rect.x > SCREEN_WIDTH + 100 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def make_sound(self):
        if self.noise:
            if self.item_name == 'monkey':
                Sound.monkey_sound(self)
            if self.item_name == 'raven':
                Sound.raven_sound(self)
            if self.item_name == 'boar':
                Sound.boar_sound(self)
            if self.item_name == 'bee':
                Sound.bee_sound(self)
        self.noise = False

    def update(self):
        self.sprite_frames()
        self.movement_enemy_current_pos()
        self.make_sound()
        self.shooting_enemy()
        self.prevent_overflow_item_group()



