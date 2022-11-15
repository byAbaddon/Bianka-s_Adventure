import pygame
from src.settings import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE, vec, check_key_pressed, key_pressed
from src.classes.class_sound import Sound


# ============================================= class Player===============================================
class Player(pygame.sprite.Sprite, Sound):
    COOLDOWN = 1000   # milliseconds cooldown
    WEAPONS_DICT = {'knife': {'cooldown_shooting': 600, 'power': 5},
                    'spear': {'cooldown_shooting': 1000, 'power': 7},
                    'axe': {'cooldown_shooting': 800, 'power': 10}
                    }
    current_weapon = '../src/assets/images/bullets/knife.png'
    current_weapon_name = current_weapon.split('/')[5][:-4]
    GRAVITY = 0.2
    SPRITE_ANIMATION_SPEED = 0.3
    JUMP_HEIGHT = -6
    PLAYER_FRICTION = -0.12
    PLAYER_SPEED = 0.4
    life = 3
    points = 0
    energy_power = 100
    is_player_dead = False
    is_player_poisoned = False
    statistics = {}
    hit_enemy_counter = 0
    AMULETS_LIST = [f'../src/assets/images/amulets/small/{x}.png' for x in range(1, 10)]  # Boss append amulet in list
    bonus_coins = 0
    bonus_statuette = 0
    player_dead_x_pos = 0
    is_player_kill_boss = False
    boss_taken_amulets = 0
    is_jump_allowed = True
    is_player_squat = False
    is_water_level = False
    is_boss_level = False
    is_bonus_level = False
    is_drive_jeep = False
    is_allowed_shooting = True

    def __init__(self, class_bullet, all_sprite_groups_dict):
        pygame.sprite.Sprite.__init__(self)
        self.class_bullet = class_bullet
        self.all_sprite_groups_dict = all_sprite_groups_dict
        self.image = pygame.image.load('../src/assets/images/player/stay/1.png')
        self.sprites_walking = [pygame.image.load(f'../src/assets/images/player/walking/{x}.png') for x in range(1, 7)]
        self.current_sprite = 0
        self.player_height_size = self.image.get_height()
        self.player_width_size = self.image.get_width()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (SCREEN_WIDTH - 650, SCREEN_HEIGHT - (self.player_height_size - 124))
        self.is_jump = False
        self.direction = vec(0, 1)  # stay 0
        self.pos = vec(self.rect.x, self.rect.y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.last_time = pygame.time.get_ticks()
        self.shot_position = self.pos
        self.WALK_LEFT_SCREEN_BORDER = self.player_width_size
        self.WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH // 3
        self.jump_limit = SCREEN_HEIGHT  # allowed jump form all position

    def movement_plyer(self):
        self.acceleration = vec(0, self.GRAVITY)  # fail gravity
        self.direction = vec(self.direction.x, self.direction.y)
        # if boss leve walk in all SCREEN_WIDTH
        if self.is_boss_level:
            self.WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH - 60

        if self.is_bonus_level:
            if self.is_drive_jeep:  # set jeep or yacht right border
                self.WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH - 105
            else:
                self.WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH - 140

        key = pygame.key.get_pressed()

        # fix border walk and jump player
        if self.pos.x < 25:
            self.pos.x = self.WALK_LEFT_SCREEN_BORDER
            self.direction = vec(1, 0)
        if self.is_jump_allowed and not self.is_bonus_level:
            # jump up
            if key[pygame.K_UP] and self.direction.y == 1 and self.direction.x != 0 and self.rect.bottom < self.jump_limit:
                Sound.player_jump(self)
                self.is_jump = True
                self.direction.y = -1
                self.velocity.y = self.JUMP_HEIGHT
                if self.direction.x == 1:
                    self.image = pygame.image.load('../src/assets/images/player/jump/1.png')
                else:
                    self.image = pygame.transform.flip(
                        pygame.image.load('../src/assets/images/player/jump/2.png'), True, False)
                # change image if player jump in Right Border
                if self.pos.x >= self.WALK_LEFT_SCREEN_BORDER and key[pygame.K_RIGHT]:
                    self.image = pygame.image.load('../src/assets/images/player/walking/5.png')

            # jump up right
            if key[pygame.K_UP] and key[pygame.K_RIGHT] and self.pos.x < self.WALK_RIGHT_SCREEN_BORDER:
                if not self.is_jump:
                    self.velocity.y = self.JUMP_HEIGHT
                self.direction = vec(1, -1)
                self.acceleration.x = self.PLAYER_SPEED
                self.is_jump = True
                self.image = pygame.image.load('../src/assets/images/player/walking/5.png')

            # jump up left
            if key[pygame.K_UP] and key[pygame.K_LEFT] and self.pos.x >= self.WALK_LEFT_SCREEN_BORDER:
                self.direction = vec(-1, -1)
                if self.pos.x <= 80:
                    self.direction.x = 1
                else:
                    self.direction.x = -1
                if not self.is_jump:
                    self.velocity.y = self.JUMP_HEIGHT
                self.acceleration.x = -self.PLAYER_SPEED
                self.is_jump = True
                self.image = pygame.transform.flip(
                    pygame.image.load('../src/assets/images/player/walking/5.png'), True, False)

        # go left
        if key[pygame.K_LEFT] and self.direction.y == 1 and self.pos.x >= self.WALK_LEFT_SCREEN_BORDER \
                and not key[pygame.K_RIGHT]:
            if self.pos.x <= self.WALK_LEFT_SCREEN_BORDER:
                self.direction.x = 1
            else:
                self.direction.x = -1
                self.image = pygame.transform.flip(self.image, True, False)
                self.acceleration.x = -self.PLAYER_SPEED

        # go right
        if key[pygame.K_RIGHT] and self.direction.y == 1 and self.pos.x <= self.WALK_RIGHT_SCREEN_BORDER \
                and not key[pygame.K_LEFT]:
            self.direction.x = 1
            self.acceleration.x = self.PLAYER_SPEED

        # squat
        if key[pygame.K_DOWN] and not key[pygame.K_RIGHT] and not key[pygame.K_LEFT] and not key[pygame.K_UP] and\
                self.direction.y == 1 and not self.is_bonus_level:
            self.is_player_squat = True
            if not self.is_water_level:  # squat only not water level
                self.acceleration = vec(0, 0)
                self.pos.y = SCREEN_HEIGHT - (GROUND_HEIGHT_SIZE - self.player_height_size // 3)
                if self.direction.x == 1:
                    self.image = pygame.image.load('../src/assets/images/player/squat/1.png')
                else:
                    self.image = pygame.transform.flip(
                        pygame.image.load('../src/assets/images/player/squat/1.png'), True, False)

        # restore image after squat
        if self.is_player_squat and not check_key_pressed(pygame.K_DOWN):
            if self.direction.x == 1:
                self.image = pygame.image.load('../src/assets/images/player/stay/1.png')
            else:
                self.image = pygame.transform.flip(
                    pygame.image.load('../src/assets/images/player/stay/1.png'), True, False)
            self.is_player_squat = False

        # running
        # if key[pygame.K_a] and self.pos.x > self.WALK_LEFT_SCREEN_BORDER:
        #     if not self.direction.y == -1 and not self.direction.y == 0:
        #         if self.direction.x == 1:
        #             self.velocity.x += 0.5
        #         elif self.direction.x == -1:
        #             self.velocity.x -= 0.5

        # =============================================================== MOVEMENT !!!
        # apply friction
        self.acceleration.x += self.velocity.x * self.PLAYER_FRICTION
        # equations of motion
        self.velocity += self.acceleration
        # set velocity in zero if player no movement
        # if abs(self.velocity.x) < 0.1:
        #     self.velocity.x = 0
        # player running
        self.pos += self.velocity + self.acceleration * self.PLAYER_SPEED
        self.rect.midbottom = self.pos
        # ============================================================================

    def shooting_payer(self):  # shooting:
        key = pygame.key.get_pressed()
        time_now = pygame.time.get_ticks()  # get time now
        # velocity is equal shooting window time
        if key[pygame.K_SPACE] and self.direction.x != 0 and abs(self.velocity.x) <= 3.0 and not self.is_bonus_level\
                and time_now - self.last_time > self.WEAPONS_DICT[self.current_weapon_name]['cooldown_shooting']\
                and self.is_allowed_shooting:
            Sound.player_shoot(self)
            self.last_time = time_now

            self.shot_position = self.rect.midright

            if self.acceleration.y <= 0:
                action = 'squat'
                y = self.shot_position[1] - 10  # get y pos form rect
            else:
                action = 'angry'
                y = self.shot_position[1] - 26  # get y pos form rect

            if self.direction.x == 1:
                x = self.shot_position[0] + 20  # get x pos form rect
                self.image = pygame.image.load(f'../src/assets/images/player/{action}/1.png')
            else:
                self.image = pygame.image.load(f'../src/assets/images/player/{action}/2.png')
                x = self.shot_position[0] - 100
                if self.acceleration.y <= 0:
                    x += 30
            bullet = self.class_bullet(self.current_weapon, x, y, self.direction)
            self.all_sprite_groups_dict['bullets'].add(bullet)

    def poisoned_player_energy_decrease(self):
        # if work have bug - weapon delay
        time_now = pygame.time.get_ticks()
        if self.is_player_poisoned and time_now - self.last_time > self.COOLDOWN:
            self.energy_power -= 1
            self.last_time = time_now

    def sprite_frames(self):
        key = pygame.key.get_pressed()
        # left and right animation
        if self.direction.y == 1 and (key[pygame.K_LEFT] or (key[pygame.K_RIGHT]) or
                                      (self.pos.x >= self.WALK_RIGHT_SCREEN_BORDER) and key[pygame.K_RIGHT]):
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites_walking):
                self.current_sprite = 1
            self.image = self.sprites_walking[int(self.current_sprite)]

    def check_ground_collide(self):
        buffer = 5  # buffer image to improve collide
        # ground and player collide
        hits = pygame.sprite.spritecollide(self, self.all_sprite_groups_dict['ground'], False)
        if hits:
            # check_ground_border
            hits_ground = hits[0]
            if not (hits_ground.rect.left > self.pos.x or self.pos.x > hits_ground.rect.right):
                # check is player head hits in bottom platform
                if self.pos.y < hits[0].rect.bottom:
                    # ground collide
                    self.pos.y = hits[0].rect.top + buffer  # buffer after collide for removing player trembling
                    self.velocity.y = 0
                    self.direction.y = 1

                    # change image after jump
                    if self.is_jump:
                        if self.direction.x == 1:
                            self.image = pygame.image.load('../src/assets/images/player/stay/1.png')
                        else:
                            self.image = pygame.image.load('../src/assets/images/player/stay/2.png')
                        self.is_jump = False

    def check_platform_collide(self):
        buffer = 6  # buffer image to improve collide
        group_items = self.all_sprite_groups_dict['items']
        for sprite in pygame.sprite.spritecollide(self, group_items, False, pygame.sprite.collide_mask):
            # print(sprite.group_name)
            if sprite.group_name in ['cloud', 'logs', 'platform']:
                if sprite.group_name == 'logs':  # fix flickering if player on the logs
                    buffer = 9
                elif sprite.group_name == 'platform':
                    buffer = 1
                # check is player head hits in bottom platform
                if self.pos.y < sprite.rect.bottom:
                    if not (sprite.rect.left > self.pos.x or self.pos.x > sprite.rect.right):
                        # ground collide
                        self.pos.y = sprite.rect.top + buffer  # buffer after collide for removing player trembling
                        self.velocity.y = 0
                        self.direction.y = 1
                        # change image after jump
                        if self.is_jump:
                            if self.direction.x == 1:
                                self.image = pygame.image.load('../src/assets/images/player/stay/1.png')
                            else:
                                self.image = pygame.image.load('../src/assets/images/player/stay/2.png')
                            self.is_jump = False
                else:
                    self.is_jump_allowed = False  # if plyer body collide cloud  disallow JUMP

    def check_item_collide(self):
        group_items = self.all_sprite_groups_dict['items']
        for sprite in pygame.sprite.spritecollide(self, group_items, False, pygame.sprite.collide_mask):
            name = sprite.item_name
            match sprite.group_name:
                case 'enemies':
                    Sound.player_enemy_hit(self)  # sound if player hit with some enemy
                    if name in ['fish', 'mouse', 'cockroach', 'cactus_ball', 'bee']:
                        self.energy_power -= 10
                        sprite.kill()
                    if name in ['raven', 'octopus', 'dragon', 'fireball', 'snowball', 'penguin', 'bird', 'bat', 'stone',
                                'crab', 'static_crab', 'vamp', 'medusa_attack']:
                        self.energy_power -= 20
                        sprite.kill()
                    if name in ['hedgehog', 'mole', 'turtle', 'seal', 'eagle_attack', 'medusa', 'lizard', 'bat_attack']:
                        self.energy_power -= 30
                        sprite.kill()
                    if name in ['monkey', 'ghost', 'snowmen', 'emu', 'dragon_big', 'stone_ball']:
                        self.energy_power -= 50
                        sprite.kill()
                    if name in ['boar', 'crocodile', 'camel', 'tiger', 'dragon_big_attack', 'knight_sword',
                                'knight_pike', 'knight_axe']:
                        self.energy_power -= 100
                        self.is_player_dead = True
                        if name == 'crocodile' or 'camel' or 'boar' or 'tiger' or 'dragon_big_attack':
                            Sound.crocodile_eat_sound(self)
                            self.kill()
                case 'mushroom':
                    Sound.add_point(self)
                    if name == 'grey':
                        self.points += 50
                    if name == 'orange':
                        self.points += 100
                    if name == 'red':
                        self.points += 200
                    if name == 'purple':
                        Sound.grab_poison_mushroom(self)
                        self.is_player_poisoned = True
                        self.energy_power -= 25
                    sprite.kill()
                    Sound.grab_item(self)
                case 'crystal' | 'diamond' | 'gnome' | 'star' | 'plant' | 'shield':
                    Sound.add_point(self)
                    if name in ['green']:
                        self.points += 100
                    if name in ['blue']:
                        self.points += 150
                    if name in ['red']:
                        self.points += 200
                    if name in ['purple']:
                        self.points += 250
                    sprite.kill()
                    Sound.grab_item(self)
                case 'bonus':
                    if name == 'coin':
                        self.bonus_coins += 1
                        Sound.grab_coin(self)
                    if name == 'statuette' or name == 'balloon':
                        self.bonus_statuette = 1
                        Sound.grab_statuette(self)
                    sprite.kill()
                case 'trap':
                    if name == 'black':
                        self.energy_power -= 20
                        Sound.snapping_trap(self)
                        Sound.player_injury(self)
                        sprite.kill()
                case 'stones' | 'cactus' | 'head':
                    self.image = pygame.image.load('../src/assets/images/player/fail/fail_right.png')
                    Sound.player_stone_hit(self)
                    sprite.rect.x -= 10
                    if name in ['big', 'big_red', 'big_ice', 'big_des', ]:
                        self.energy_power -= 3  # X 2
                    if name in ['medium', 'medium_red', 'medium_ice', 'medium_des', 'k1', 'k2', 'k3', 'k4']:
                        self.energy_power -= 2
                    if name in ['small', 'small_red', 'small_ice', 'small_des']:
                        self.energy_power -= 1
                    return
                case 'decor':
                    if name == 'spear':
                        self.current_weapon = '../src/assets/images/bullets/spear.png'
                        self.current_weapon_name = 'spear'
                        Sound.player_get_weapon(self)
                        sprite.kill()
                    if name == 'axe':
                        self.current_weapon = '../src/assets/images/bullets/axe.png'
                        self.current_weapon_name = 'axe'
                        Sound.player_get_weapon(self)
                        sprite.kill()
            # -------------------------------------------------create statistics
            ignore_group_list = ['ground',  'decor', 'signs', 'stones', 'cactus', 'head', 'logs', 'cloud', 'platform',
                                 'trap', 'enemies']
            if sprite.group_name not in ignore_group_list:
                if sprite.group_name not in self.statistics:  # add item to statistics dict if not have key
                    self.statistics[sprite.group_name] = {name: 1}
                else:
                    if name not in self.statistics[sprite.group_name]:
                        self.statistics[sprite.group_name][name] = 0
                    self.statistics[sprite.group_name][name] += 1
            # print(self.statistics)

    def check_bullets_collide(self):
        bullets_group = self.all_sprite_groups_dict['bullets']
        items_group = self.all_sprite_groups_dict['items']
        sprite = pygame.sprite.groupcollide(bullets_group, items_group, False, False, pygame.sprite.collide_mask)
        for bullet, item in sprite.items():
            item = item[0]
            # add bullet effect explosion
            if item.group_name not in ['signs', 'decor', 'wall_decor']:  # ignore bullet collide
                hit_explosion = pygame.image.load('../src/assets/images/explosion/explosion.png')
                if self.current_weapon_name == 'spear':
                    SCREEN.blit(hit_explosion, (bullet.rect.x + 45, bullet.rect.y + 25))
                else:
                    SCREEN.blit(hit_explosion, (bullet.rect.x + 20, bullet.rect.y))  # bullet.rect.topleft
            match item.group_name:
                case 'logs' | 'cloud':
                    Sound.bullet_hit(self)
                    bullet.kill()
                case 'mushroom' | 'crystal' | 'diamond' | 'gnome' | 'star' | 'plant' | 'shield':
                    Sound.bullet_hit(self)
                    bullet.kill()
                    item.kill()
                case 'stones' | 'head':
                    Sound.bullet_ricochet(self)
                    bullet.kill()
                case 'cactus':
                    if item.group_name not in self.statistics:  # add item to statistics dict if not have key
                        self.statistics[item.group_name] = {item.item_name: 1}
                    else:
                        if item.item_name not in self.statistics[item.group_name]:
                            self.statistics[item.group_name][item.item_name] = 0
                        self.statistics[item.group_name][item.item_name] += 1
                    self.points += 100
                    bullet.kill()
                    item.kill()
                case 'trap':
                    if item.group_name not in self.statistics:
                        self.statistics[item.group_name] = {item.item_name: 1}
                    self.statistics[item.group_name][item.item_name] += 1
                    Sound.snapping_trap(self)
                    self.points += 100
                    bullet.kill()
                    item.kill()
                case 'bonus':
                    if 'coin' or 'statuette':
                        Sound.bullet_statuette_hit(self)
                        bullet.kill()
                        item.kill()
                case 'enemies':
                    if item.item_name == 'stone_ball' or item.item_name == 'fireball':
                        Sound.bullet_ricochet(self)
                        bullet.kill()
                    if item.item_name in ['fish', 'mole',  'crab', 'static_crab', 'bee', 'bird', 'cactus_ball']:
                        self.points += 100
                        Sound.bullet_kill_enemy(self)
                        item.kill()
                        bullet.kill()
                    if item.item_name in ['hedgehog', 'dragon', 'turtle', 'cockroach', 'snowmen', 'lizard', 'vamp']:
                        self.points += 200
                        Sound.bullet_kill_enemy(self)
                        item.kill()
                        bullet.kill()
                    if item.item_name in ['mouse', 'octopus', 'raven', 'butterfly', 'ghost', 'penguin', 'seal', 'bird',
                                          'eagle_attack', 'medusa', 'medusa_attack', 'emu', 'bat', 'bat_attack']:
                        self.points += 300
                        Sound.bullet_kill_enemy(self)
                        item.kill()
                        bullet.kill()
                    if item.item_name in ['boar', 'monkey', 'crocodile', 'camel', 'tiger', 'dragon_big',
                                          'dragon_big_attack']:
                        bullet.kill()
                        if bullet.item_name == 'spear':
                            self.hit_enemy_counter += 1
                        elif bullet.item_name == 'axe':
                            self.hit_enemy_counter += 2
                        self.hit_enemy_counter += 1

                        if self.hit_enemy_counter >= 3:
                            self.hit_enemy_counter = 0
                            self.points += 500
                            bullet.kill()
                            item.kill()
                            if item.group_name not in self.statistics:  # add item to statistics dict if not have key
                                self.statistics[item.group_name] = {item.item_name: 1}
                            else:
                                if item.item_name not in self.statistics[item.group_name]:
                                    self.statistics[item.group_name][item.item_name] = 0
                                self.statistics[item.group_name][item.item_name] += 1
                        Sound.bullet_kill_boar(self)
                    if item.item_name == 'knight_sword' or 'knight_pike' or 'knight_axe':
                        sprite = pygame.sprite.spritecollide(item, bullets_group, True, pygame.sprite.collide_mask)
                        if sprite:
                            for hit_point in sprite:
                                if 400 <= hit_point.rect.topleft[1] <= 442:  # head shoot
                                    Sound.bullet_player_hit_knight_face(self)
                                    self.hit_enemy_counter += 1
                                    if self.hit_enemy_counter == 3:
                                        self.points += 1000
                                        Sound.knight_dead_sound(self)
                                        item.kill()
                                        self.hit_enemy_counter = 0
                                        if item.group_name not in self.statistics:  # add item to dict if not have key
                                            self.statistics[item.group_name] = {item.item_name: 1}
                                        else:
                                            if item.item_name not in self.statistics[item.group_name]:
                                                self.statistics[item.group_name][item.item_name] = 0
                                            self.statistics[item.group_name][item.item_name] += 1
                                    bullet.kill()
                                else:
                                    Sound.bullet_player_hit_knight_armor(self)  # body soot

                    ignore_group_list = ['stone_ball', 'fireball', 'decor', 'signs', 'stones', 'head', 'logs', 'cloud',
                                         'platform', 'bonus']
                    ignore_items_list = ['boar', 'monkey', 'crocodile', 'camel', 'tiger', 'dragon_big', 'stone_ball',
                                          'fireball', 'knight_sword', 'knight_pike', 'knight_axe']
                    if item.group_name not in ignore_group_list and item.item_name not in ignore_items_list:
                        if item.group_name not in self.statistics:  # add item to statistics dict if not have key
                            self.statistics[item.group_name] = {item.item_name: 1}
                        else:
                            if item.item_name not in self.statistics[item.group_name]:
                                self.statistics[item.group_name][item.item_name] = 0
                            self.statistics[item.group_name][item.item_name] += 1
                    # print(self.statistics)
                    # print(item.item_name, item.group_name)

    def check_enemy_bullets_collide(self):
        bullets_group = self.all_sprite_groups_dict['bullets']
        for sprite in pygame.sprite.spritecollide(self, bullets_group, False, pygame.sprite.collide_mask):
            match sprite.item_name:
                case 'egg' | 'coconut' | 'bone' | 'snowball' | 'skull' | 'spit' | 'fire_spit' | 'arrow' | 'medusa_spit':
                    sprite.kill()
                    Sound.enemy_bullet_hit_player_head(self)
                    self.energy_power -= 10
                case 'magic':
                    sprite.kill()
                    Sound.player_injury_scream(self)
                    self.energy_power -= 20

    def check_player_and_enemy_bullets_collide(self):
        bullets_group = self.all_sprite_groups_dict['bullets']
        for bullet in bullets_group:
            if bullet.item_name == 'magic':
                return
            sprite_collide = pygame.sprite.spritecollide(bullet, bullets_group, False)
            #if len(sprite_collide) == 1:  hit with self.
            if len(sprite_collide) > 1:
                for sprite in sprite_collide:
                    Sound.bullet_hit(self)
                    hit_explosion = pygame.image.load('../src/assets/images/explosion/explosion.png')
                    SCREEN.blit(hit_explosion, bullet.rect.topleft)
                    sprite.kill()

    def check_is_energy_player(self):
        if self.energy_power <= 0 and not self.is_player_dead:
            if self.energy_power < 0:
                self.energy_power = 0  # set low boundary draw energy bar
            self.player_dead_x_pos = self.pos.x
            self.image = pygame.image.load('../src/assets/images/player/dead/dead.png')  # test
            Sound.player_dead(self)
            # self.kill()
            self.is_player_dead = True
            # print(1.1)
            return True

    def check_is_player_fail_out_of_screen(self):
        if self.pos.y > SCREEN_HEIGHT and not self.is_player_dead:
            self.player_dead_x_pos = self.pos.x
            self.kill()
            self.is_player_dead = True
            print(1)
            return True

    def check_bonus_level_collide(self):
        bonus_group = self.all_sprite_groups_dict['bonus']
        self.rect.y = SCREEN_HEIGHT - 150
        sprites = pygame.sprite.spritecollide(self, bonus_group, False, pygame.sprite.collide_mask)
        self.rect.y -= 50
        # pygame.draw.rect(SCREEN, 'red', self.rect)
        if sprites and not self.is_player_dead:
            for sprite in sprites:
                if sprite.item_name == 'coin_small':
                    self.bonus_coins += 1
                    Sound.coin_fail(self)
                    sprite.kill()
                elif sprite.item_name == 'star_small':
                    self.bonus_coins += 1
                    Sound.grab_star(self)
                    sprite.kill()

                if sprite.item_name == 'bomb' or sprite.item_name == 'comet':
                    pygame.event.clear()  # clear all events in queue
                    SCREEN.fill(pygame.Color('black'))
                    Sound.stop_all_sounds()
                    Sound.explosion(self)  # play sound bomb
                    for i in range(17):
                        increase_pic = 100 * i
                        exp = pygame.image.load('../src/assets/images/explosion/big_exp_1.jpeg')
                        explosion = pygame.transform.scale(exp, (increase_pic, increase_pic))
                        central_pos = explosion.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                        SCREEN.blit(explosion, central_pos)
                        pygame.display.update()
                        pygame.time.delay(100)
                    self.is_player_dead = True

    def update(self):
        self.check_is_energy_player()
        self.check_is_player_fail_out_of_screen()  # return True or False
        pygame.mask.from_surface(self.image)  # create mask image
        if not self.is_player_dead:
            self.sprite_frames()  # don't change position !!!
            self.movement_plyer()
            self.shooting_payer()
        self.check_ground_collide()
        self.check_item_collide()
        self.check_bullets_collide()
        self.check_enemy_bullets_collide()
        # self.poisoned_player_energy_decrease()
        self.check_platform_collide()
        self.check_player_and_enemy_bullets_collide()
        if self.is_bonus_level:
            self.check_bonus_level_collide()

    # ============================================ RESET PLAYER DATA ====================================
    # reset For current game
    def reset_current_player_data(self):
        self.energy_power = 101  # add 1 to for fix full energy
        self.bonus_coins = 0
        self.bonus_statuette = 0
        self.player_dead_x_pos = 0
        self.image = pygame.image.load('../src/assets/images/player/stay/1.png')
        self.rect.center = (SCREEN_WIDTH - 700, SCREEN_HEIGHT - (self.player_height_size - GROUND_HEIGHT_SIZE))
        self.direction = vec(0, 1)  # stay 0
        self.pos = vec(self.rect.x, self.rect.y)
        self.jump_limit = SCREEN_HEIGHT  # allowed jump form all position
        self.is_player_dead = False
        self.is_player_poisoned = False
        self.is_player_kill_boss = False
        self.is_jump = False
        self.is_jump_allowed = True
        self.is_bonus_level = False
        self.is_player_squat = False
        self.is_water_level = False
        self.is_drive_jeep = False
        self.is_allowed_shooting = True

    # RESET TO NEW GAME
    def reset_all_player_data_for_new_game(self):
        self.current_weapon = '../src/assets/images/bullets/knife.png'
        self.life = 3
        self.points = 0
        self.energy_power = 100
        self.bonus_statuette = 0
        self.bonus_coins = 0
        self.bonus_coins = 0
        self.bonus_statuette = 0
        self.statistics = {}
        self.hit_enemy_counter = 0
        self.boss_taken_amulets = 0
        self.player_dead_x_pos = 0
        self.image = pygame.image.load('../src/assets/images/player/stay/1.png')
        self.rect.center = (SCREEN_WIDTH - 700, SCREEN_HEIGHT - (self.player_height_size - GROUND_HEIGHT_SIZE))
        self.direction = vec(0, 1)  # stay 0
        self.pos = vec(self.rect.x, self.rect.y)
        self.jump_limit = SCREEN_HEIGHT  # allowed jump form all position
        self.is_player_dead = False
        self.is_player_poisoned = False
        self.is_player_kill_boss = False
        self.is_boss_level = False
        self.is_jump = False
        self.is_jump_allowed = True
        self.is_bonus_level = False
        self.is_player_squat = False
        self.is_water_level = False
        self.is_drive_jeep = False
        self.is_allowed_shooting = True
