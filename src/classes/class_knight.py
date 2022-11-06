import pygame
from src.settings import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE, vec, randrange
from src.classes.class_sound import Sound


class Knight(pygame.sprite.Sprite, Sound):
    SPRITE_ANIMATION_SPEED = 0.3
    WALK_LEFT_SCREEN_BORDER = 20  # is knight w_size
    WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH - 20
    WALK_SPEED = 3
    JUMP_HEIGHT = -6
    COOLDOWN = 2000  # milliseconds
    COOLDOWN_MAGIC = 9000 # milliseconds
    last_time = pygame.time.get_ticks()
    last_time_magic = pygame.time.get_ticks()
    time_counter = 0
    visited = False
    energy_power = 2
    is_idle = True
    is_walk = False
    is_run = False
    is_jump = False
    is_attack = False
    is_dead = False
    is_sound = False
    player_dead_x_pos = 0
    is_boss_level_complete = False
    is_boss_kill_player = False

    def __init__(self, class_bullet, all_sprite_groups_dict, player):
        pygame.sprite.Sprite.__init__(self)
        self.class_bullet = class_bullet
        self.all_sprite_groups_dict = all_sprite_groups_dict
        self.player = player
        self.image = pygame.image.load('../src/assets/images/boss_knight/idle/1.png')
        self.sprites_knight = [pygame.image.load(f'../src/assets/images/boss_knight/idle/{x}.png') for x in range(1, 11)]
        self.current_sprite = 0
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midbottom = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE + 4)
        self.direction = vec(-1, 1)  # stay/idle 0

    def knight_movie(self):
        if not self.is_dead and not self.is_boss_kill_player and self.is_walk or self.is_attack:
            # ---------------------------------------- first knight scream sound
            if not self.is_sound and self.is_walk:
                Sound.knight_scream(self)
                # change list ot pic sprite USING scope BOOLEAN SOUND TO PREVENT falling FPS
                self.sprites_knight = [pygame.image.load(f'../src/assets/images/boss_knight/walk/{x}.png') for x in range(1, 11)]
                self.is_sound = True

            if self.is_sound and self.is_attack:
                if self.is_sound:
                    self.WALK_SPEED = 4
                    Sound.boss_attack(self)
                    # change list ot pic sprite USING scope BOOLEAN SOUND TO PREVENT falling FPS
                    self.sprites_knight = [pygame.image.load(f'../src/assets/images/boss_knight/attack/{x}.png')
                                           for x in range(1, 11)]
                    self.is_sound = False

            # ---------------------------------------- go left
            if self.direction.x == -1:
                self.rect.x -= self.WALK_SPEED
                if self.rect.x <= 150:
                    self.direction.x = 1
            # --------------------------------------- go right
            if self.direction.x == 1:
                self.rect.x += self.WALK_SPEED
                if self.rect.x >= randrange(500, SCREEN_WIDTH) and self.is_walk:
                    self.direction.x = -1
                elif self.rect.x >= randrange(400, SCREEN_WIDTH - 100) and self.is_attack:
                    self.direction.x = -1

    def knight_dead(self):
        if not self.is_dead:
            self.energy_power = 0
            Sound.knight_dead(self)
            # add amulets number to player list
            self.player.boss_taken_amulets += 1
            self.is_dead = True
        self.image = pygame.image.load('../src/assets/images/boss_knight/dead/9.png')
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - self.image.get_height() // 2

        # create amulet after knight dead
        amulet = pygame.image.load(f'../src/assets/images/amulets/big/crown_middle.png')
        img_rect = amulet.get_bounding_rect(min_alpha=1)
        img_rect.center = [SCREEN_WIDTH - 185, SCREEN_HEIGHT // 2 + 10]
        SCREEN.blit(amulet, img_rect.center)

        # check collide player and amulet
        get_amulet = self.player.rect.colliderect(img_rect)
        if get_amulet:
            # self.reset_knife_data()  # RESET ALL KNIGHT DATA
            Sound.grab_amulets(self)
            self.player.is_player_kill_boss = True  # return info to player class if boss death and take amulet
            self.is_boss_level_complete = True

    def sprite_frames(self):
        if self.direction.y == 1:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites_knight):
                self.current_sprite = 1
            self.image = self.sprites_knight[int(self.current_sprite)]

    def check_players_bullet_collide(self):
        bullets_group = self.all_sprite_groups_dict['bullets']
        sprite = pygame.sprite.spritecollide(self, bullets_group, True, pygame.sprite.collide_mask)
        if sprite:
            for hit_point in sprite:
                # add bullet effect explosion
                hit_explosion = pygame.image.load('../src/assets/images/explosion/exp_1.png')
                SCREEN.blit(hit_explosion, hit_point.rect.topleft)

                if 400 <= hit_point.rect.topleft[1] <= 442:  # head shoot
                    self.is_walk = True
                    self.is_idle = False
                    Sound.bullet_player_hit_knight_face(self)
                    # self.energy_power -= self.player.WEAPONS_DICT[self.player.current_weapon_name]['power']
                    self.energy_power -= 1
                else:
                    Sound.bullet_player_hit_knight_armor(self)  # body soot

    def check_players_and_boss_collide(self):
        player_group = self.all_sprite_groups_dict['player']
        knight_group = self.all_sprite_groups_dict['knight']

        hit = pygame.sprite.groupcollide(player_group, knight_group, False, False, pygame.sprite.collide_mask)
        if hit and not self.is_dead:
            self.player.is_allowed_shooting = False
            self.is_boss_kill_player = True
            self.is_walk = False
            self.is_attack = False
            self.image = pygame.image.load('../src/assets/images/boss_knight/idle/1.png')
            if not self.visited:
                Sound.player_dead(self)
                self.player_dead_x_pos = self.player.rect.x
                self.visited = True
        if self.visited:
            self.player.rect.center = [self.player_dead_x_pos, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE + 10]
            self.player.image = pygame.image.load('../src/assets/images/player/dead/dead_back.png')
            time_now = pygame.time.get_ticks()
            if time_now - self.last_time > self.COOLDOWN:  # pause after dead
                self.last_time = time_now
                self.time_counter += 1
                if self.time_counter == 2:
                    self.player.energy_power = 0
                    Sound.stop_all_sounds()
                    Sound.player_lost_live_music(self)
                    self.player.life -= 1
                    self.player.is_player_dead = True

    def energy_boss_watcher(self):
        if self.energy_power <= 100:  # switch to attack sprite option
            self.is_walk = False
            self.is_attack = True

    def witch_magic(self):
        if self.energy_power < 150 and not self.is_idle:
            bullet = self.class_bullet('../src/assets/images/bullets/magic.png', 305, 265, self.player.pos, 1)
            time_now = pygame.time.get_ticks()
            if time_now - self.last_time > self.COOLDOWN - 1000 and self.is_attack:  # create sound attack
                self.last_time = time_now
                Sound.knight_sword_attack(self)
            if time_now - self.last_time_magic > self.COOLDOWN_MAGIC:  # create magic
                self.last_time_magic = time_now
                self.all_sprite_groups_dict['bullets'].add(bullet)
                Sound.witch_magic_effect(self)

    def update(self,):
        self.sprite_frames()
        self.check_players_bullet_collide()
        self.check_players_and_boss_collide()
        self.energy_boss_watcher()
        if self.energy_power <= 0:
            self.knight_dead()
            if self.energy_power < 0:
                self.energy_power = 0
        else:
            self.knight_movie()
            self.witch_magic()

    # ======================================reset knight data
    def reset_knife_data(self):
        self.energy_power = 200  # 200
        self.time_counter = 0
        self.is_walk = False
        self.is_run = False
        self.is_jump = False
        self.is_attack = False
        self.is_dead = False
        self.is_sound = False
        self.player_dead_x_pos = 0
        self.is_boss_level_complete = False
        self.visited = False
        self.image = pygame.image.load('../src/assets/images/boss_knight/idle/1.png')
        self.sprites_knight = [pygame.image.load(f'../src/assets/images/boss_knight/idle/{x}.png') for x in range(1, 11)]
        self.current_sprite = 0
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midbottom = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE + 4)
        self.direction = vec(-1, 1)  # stay/idle 0
        self.is_boss_kill_player = False





