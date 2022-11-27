import pygame.time

from settings import *
from classes.class_background import Background
from classes.class_table import Table
from src.classes.class_sound import Sound
from state_classes import Intro, Menu, Story, LevelStatistic, PlayerDead, Epilogue
from classes.class_player import Player
from classes.class_knight import Knight
from classes.class_ground import Ground
from classes.class_bullet import Bullet
from classes.class_item import Item
from classes.class_enemy import Enemy
from classes.class_cloud import Cloud
from classes.class_log import Log
from classes.class_bonus import Bonus
from classes.class_fall_effect import FallEffect
from src.score.crud import ranking_manipulator, post

# ================================================================= TEST imported classes
# print(dir(Menu))

# ======================================================================== create Sprite groups
background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
knight_group = pygame.sprite.GroupSingle()
ground_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
bonus_group = pygame.sprite.GroupSingle()
gen_statistics_group = pygame.sprite.GroupSingle()
fall_effect_group = pygame.sprite.GroupSingle()


# add to all_sprite_groups   /items group included enemy/
all_spite_groups_dict = {'player': player_group, 'knight': knight_group, 'bullets': bullets_group,
                         'ground': ground_group, 'items': item_group, 'bonus': bonus_group,
                         'fall_effect': fall_effect_group}

# ======================================================================= initialize  Classes

player = Player(Bullet, all_spite_groups_dict)
knight = Knight(Bullet, all_spite_groups_dict, player)
ground = Ground()
background = Background()


# add to group
player_group.add(player)
knight_group.add(knight)
ground_group.add(ground)

# variables
asg = all_spite_groups_dict
S_W = SCREEN_WIDTH
S_H = SCREEN_HEIGHT
G_H_S = GROUND_HEIGHT_SIZE
T_F_S = TOP_FRAME_SIZE


# Game State
class GameState(Sound):
    COOLDOWN = 2000  # milliseconds
    delay_count = 2000
    start_timer = pygame.time.get_ticks()
    count_visit = 0
    amulets_counter = 0
    input_text = ''
    col_counter = 0
    gen_col_spacer = 0
    gen_row_spacer = 0
    is_visited = False
    is_final_statistics = False
    current_list = []
    ignor_keys_list = []

    def __init__(self, player_data, knight_data, background_data):
        self.state = 'intro'
        self.current_music = Sound.intro_music(self)
        self.is_music_play = False
        self.background = None
        self.is_bg_created = False
        self.area = 1
        self.level = 1
        self.boss_number = 1
        self.level_reader_row = 1  # 1
        self.player_data = player_data
        self.knight_data = knight_data
        self.background_data = background_data
        self.bonus_pts = 0
        self.is_add_bonus = False
        self.is_start_new_game = False
        self.is_in_water = False
        self.is_start_area = False
        self.count = 0
        self.ranking_list = ranking_manipulator()

    def start_game(self):
        self.is_visited = False
        # ------------------------- MAKE PAUSE GAME
        if key_pressed(pygame.K_p):
            Sound.btn_click(self)
            self.state = 'pause'
        # ------------------------- SHOW STATISTICS REAL TIME
        if key_pressed(pygame.K_s):
            Sound.btn_click(self)
            self.state = 'real_time_statistics'
        # ------------------------- SHOW CREDITS
        if key_pressed(pygame.K_c):
            Sound.btn_click(self)
            self.state = 'credits'
        # ------------------top display frame
        table.update()
        # -----------------------------------------------
        self.bonus_pts = 0  # reset pts
        # player.is_boss_level = False  # set player walking border to 1/3 S_W

        # =============================================== RESET ALL DATA IF START NEW GAME
        if self.is_start_new_game:  # reset all old data
            self.is_start_new_game = False
            Sound.stop_all_sounds()
            table.life_counter = 0
            [all_spite_groups_dict[group].empty() for group in all_spite_groups_dict]
            all_spite_groups_dict['player'].add(player)
            all_spite_groups_dict['knight'].add(knight)
            all_spite_groups_dict['ground'].add(ground)
            self.player_data.reset_all_player_data_for_new_game()  # reset all player data
            self.knight_data.reset_knife_data()  # reset all knight data
            self.level = 1
            self.area = 1
            self.boss_number = 1
            self.level_reader_row = 1
            self.bonus_pts = 0
            self.count = 0
            self.count_visit = 0
            self.amulets_counter = 0
            self.is_add_bonus = False
            self.is_in_water = False
            self.background = None
            self.is_start_area = False
            self.player_data.is_water_level = False
            self.ranking_list = []
            self.input_text = ''
            self.gen_col_spacer = 0
            self.gen_row_spacer = 0
            self.is_visited = False
            self.is_final_statistics = False
            self.current_list = []
            self.ignor_keys_list = []
            self.col_counter = 0
        # --------------------------------------draw current FPS
        if int(CLOCK.get_fps()) >= 55:
            text_creator(f'FPS: {int(CLOCK.get_fps())}', 'dodgerblue1', 250, 20, 22)
        else:
            text_creator(f'FPS: {int(CLOCK.get_fps())}', 'brown3', 250, 20, 22)
        # ++++++++++++++++++++++++++++++ developer utils +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # text_creator(f'FPS {int(CLOCK.get_fps())}', 'white', 10, 5, 25)
        # text_creator(f'Direction: x= {int(player.direction.x)} y= {int(player.direction.y)}', 'white', 90, 15, 22)
        # text_creator(f'Pos: x= {int(player.pos.x)} y= {int(player.pos.y)}', 'white', 86, 33, 22)
        # text_creator(f'Vel: x= {player.velocity.x:.2f} y= {player.velocity.y:.2f} ', 'white', 90, 50, 22)
        # text_creator(f'Acc: x= {player.acceleration.x:.2f} y= {player.acceleration.y:.2f}', 'white', 90, 70, 22)
        # text_creator(f'MousePos: x= {pygame.mouse.get_pos()}', 'white', 490, 5)

        # ================================ create enemy classes
        def enemy_creator(enemy_name):
            if enemy_name == 'enemy_bee':
                b1 = Enemy(Bullet, asg, background, '../src/assets/images/enemies/bee/1.png',
                           S_W, S_H - (G_H_S + player.image.get_height() // 2), 2, True, False,
                           '../src/assets/images/enemies/bee/1.png', 0, 4)
                b2 = Enemy(Bullet, asg, background, '../src/assets/images/enemies/bee/1.png',
                           S_W + 40, S_H - (G_H_S + player.image.get_height() // 2 - 40), 2, True, False,
                           '../src/assets/images/enemies/bee/1.png', 0, 4)
                return b1, b2
            if enemy_name == 'enemy_raven':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/raven/1.png',
                             S_W, T_F_S + 100, 3, True, True, '../src/assets/images/bullets/egg.png', 1.4, 5)
            if enemy_name == 'enemy_monkey':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/monkey/monkey.png',
                             S_W, 150, 5, True, True, '../src/assets/images/bullets/coconut.png', 1)
            if enemy_name == 'enemy_hedgehog':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/hedgehog/hedgehog.png',
                             S_W, S_H - G_H_S - 5, 1)
            if enemy_name == 'enemy_static_hedgehog':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/hedgehog/hedgehog.png',
                             S_W, S_H - G_H_S - 5, 0)
            if enemy_name == 'enemy_boar':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/boar/1.png',
                             S_W, S_H - G_H_S - 32, 3, True, False, None, None, 8)
            if enemy_name == 'enemy_mouse':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/mouse/1.png',
                             S_W, S_H - G_H_S - 2, 5, True, False, '', 0, 3)
            if enemy_name == 'enemy_static_mole':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/mole/mole.png',
                             S_W, S_H - G_H_S - 2, 0, True)
            if enemy_name == 'enemy_static_crab' or enemy_name == 'enemy_crab':
                type_enemy = 'crab'
                if len(enemy_name.split('_')) == 3:
                    type_enemy = 'static_crab'
                return Enemy(Bullet, asg, background, f'../src/assets/images/enemies/{type_enemy}/1.png',
                             S_W, S_H - G_H_S - 20, 0, True, False, None, None, 3)
            if enemy_name == 'enemy_butterfly':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/butterfly/1.png',
                             S_W, T_F_S + 100, 1, False, False, None, None, 6)
            if enemy_name == 'enemy_fish':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/fish/1.png',
                             S_W, S_H - 200, 1, True, False, None, 0, 0)
            if enemy_name == 'enemy_octopus':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/octopus/1.png',
                             S_W, S_H, 3, True, False, None, None, 0, True)
            if enemy_name == 'enemy_dragon':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/dragon/1.png',
                             S_W, S_H - G_H_S - 5, 2, True, False, None, None, 7)
            if enemy_name == 'enemy_vulture':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/vulture/1.png',
                             S_W, T_F_S + 50, 2, True, True, '../src/assets/images/bullets/bone.png', 1, 9)
            if enemy_name == 'enemy_eagle':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/eagle/1.png',
                             S_W, T_F_S + 150, 3, True, True, '../src/assets/images/bullets/skull.png', 1, 9)
            if enemy_name == 'enemy_eagle_attack':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/eagle_attack/1.png',
                             S_W, T_F_S + 150, 3, True, None, None, 0, 10)
            if enemy_name == 'enemy_bat_attack':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/bat_attack/1.png',
                             S_W, T_F_S + 170, 2, True, None, None, 0, 5)
            if enemy_name == 'enemy_bat':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/bat/1.png',
                             S_W, S_H - G_H_S - 130, 3, True, None, None, 0, 4)
            if enemy_name == 'enemy_bird' or enemy_name == 'enemy_bird_low':
                y_pos = T_F_S + 60
                if enemy_name == 'enemy_bird_low':
                    y_pos = S_H - G_H_S - 110
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/bird/1.png',
                             S_W, y_pos, 2, True, False, None, 0, 8)
            if enemy_name == 'enemy_turtle':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/turtle/1.png',
                             S_W, S_H - G_H_S - 15, 1, True, False, None, None, 8)
            if enemy_name == 'enemy_monster':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/monster/1.png',
                             S_W, S_H - G_H_S - 40, 1, True, False, None, None, 24)
            if enemy_name == 'enemy_fireball':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/fireball/1.png',
                             S_W // 2, 115, 2, True, None, None, 0, 0, True)
            if enemy_name == 'enemy_cockroach':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/cockroach/1.png',
                             S_W, S_H - G_H_S - 2, 2, True, None, None, 0, 8)
            if enemy_name == 'enemy_ghost':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/ghost/1.png',
                             S_W, 200, 1, True, None, None, 0, 6)
            if enemy_name == 'enemy_penguin':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/penguin/1.png',
                             S_W, S_H - G_H_S - 20, 2, True, False, None, None, 8)
            if enemy_name == 'enemy_seal':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/seal/1.png',
                             S_W, S_H - G_H_S - 20, 2, True, False, None, None, 5)
            if enemy_name == 'enemy_snowmen':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/snowmen/1.png', S_W,
                             S_H - G_H_S - 40, 0, True, True, '../src/assets/images/bullets/snowball.png', 2, 0)
            if enemy_name == 'enemy_medusa':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/medusa/4.png',
                             S_W, S_H - G_H_S - 28, 0, True, False, None, None, 4)
            if enemy_name == 'enemy_crocodile':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/crocodile/1.png',
                             S_W, S_H - G_H_S - 25, 0, True,)
            if enemy_name == 'enemy_medusa_attack':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/medusa_attack/6.png', S_W,
                             S_H - G_H_S - 28, 0, True, True, '../src/assets/images/bullets/medusa_spit.png', 2, 0)
            if enemy_name == 'enemy_camel':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/camel/1.png',
                             S_W, S_H - G_H_S - 35, 1, True, True, '../src/assets/images/bullets/spit.png', 2, 8)
            if enemy_name == 'enemy_cactus_ball':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/cactus_ball/1.png',
                             S_W, S_H - G_H_S - 10, 2, False, False, None, None, 6)
            if enemy_name == 'enemy_stone_ball':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/stone_ball/1.png',
                             S_W, S_H - G_H_S - 20, 2, True, None, None, 0, 5)
            if enemy_name == 'enemy_lizard':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/lizard/1.png',
                             S_W, S_H - G_H_S - 17, 2, True, False, None, None, 8)
            if enemy_name == 'enemy_emu':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/emu/1.png',
                             S_W, S_H - G_H_S - 17, 3, True, False, None, None, 6)
            if enemy_name == 'enemy_tiger':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/tiger/1.png',
                             S_W, S_H - G_H_S - 24, 1, True, False, None, None, 11)
            if enemy_name == 'enemy_dragon_big':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/dragon_big/1.png',
                             S_W, S_H - G_H_S - 20, 2, True, False, None, None, 6)
            if enemy_name == 'enemy_dragon_big_attack':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/dragon_big_attack/5.png',
                             S_W, S_H - G_H_S - 46, 0, True, True, '../src/assets/images/bullets/fire_spit.png', 2, 0)
            if enemy_name == 'enemy_shooter':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/shooter/1.png',
                             S_W, 122, 0, True, True, '../src/assets/images/bullets/arrow.png', 2, 0, True)
            if enemy_name == 'enemy_vamp':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/vamp/1.png',
                             S_W // 2, 115, 2, True, None, None, 0, 0, True)
            if enemy_name == 'enemy_knight_sword' or 'enemy_knight_pike' or 'enemy_knight_axe':
                knight_type = ''
                sprite = 0
                if enemy_name == 'enemy_knight_sword':
                    knight_type = 'knight_sword'
                    sprite = 8
                elif enemy_name == 'enemy_knight_pike':
                    knight_type = 'knight_pike'
                    sprite = 4
                elif enemy_name == 'enemy_knight_axe':
                    knight_type = 'knight_axe'
                    sprite = 3

                return Enemy(Bullet, asg, background, f'../src/assets/images/enemies/{knight_type}/1.png',
                             S_W, S_H - G_H_S - 55, 0, True, False, None, None, sprite, True)

        # ================================ create cloud platform classes
        def platform_creator(v_type):

            if v_type == 'cloud/small' or v_type == 'cloud/small_low':
                pic_cloud = '../src/assets/images/cloud/small.png'
            else:
                pic_cloud = '../src/assets/images/cloud/static.png'
            if v_type == 'cloud/static' or v_type == 'cloud/small':
                return Cloud(self.player_data, self.background, pic_cloud, S_W, S_H - 280, True, 0, 'static', 0)
            if v_type == 'cloud/left_right':
                return Cloud(self.player_data, self.background, pic_cloud, S_W, S_H - 200, False, 2, 'left_right', 200)
            if v_type == 'cloud/up_down':
                return Cloud(self.player_data, self.background, pic_cloud, S_W, S_H - 160, False, 2, 'up_down', 210)
            if v_type == 'cloud/fail':
                return Cloud(self.player_data, self.background, pic_cloud, S_W, S_H - 280, False, 1, 'fail', 0)
            if v_type == 'cloud/low':
                return Cloud(self.player_data, self.background, pic_cloud, S_W, S_H - 150, True, 0, 'static', 0)
            if v_type == 'cloud/small_low':
                return Cloud(self.player_data, self.background, pic_cloud, S_W, S_H - 150, True, 0, 'static', 0)

            # ================================ create logs
            if v_type.split('/')[0] == 'logs':
                pic_log = f'../src/assets/images/logs/{v_type.split("/")[1]}.png'
                return Log(self.player_data, pic_log, S_W, S_H - 55, True)
            # ================================ create stone platform
            if v_type.split('/')[0] == 'platform':
                pic_log = f'../src/assets/images/platform/{v_type.split("/")[1]}.png'
                return Log(self.player_data, pic_log, S_W, S_H - 48, True)

        # function sprite creator
        def sprite_creator(dictionary, input_class=None, group_class=None):
            # ---------create
            for k, v in dictionary.items():  # t: 'item pic'
                if k == int(self.background.distance_mt):
                    if v.split('_')[0] == 'enemy':  # check is enemy
                        # ---------------------------------------------------------- create new class from enemy_name
                        new_enemy_class = enemy_creator(enemy_name=v)
                        # add to item group
                        group_class.add(new_enemy_class)
                    elif v.split('/')[0] == 'cloud' or v.split('/')[0] == 'logs' or v.split('/')[0] == 'platform':
                        # create new class from cloud platform
                        new_platform_class = platform_creator(v_type=v)
                        # add to item group
                        group_class.add(new_platform_class)
                    else:
                        if v.split('/')[0] == 'ships':  # -------------------------- change item position
                            new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, 250)
                        elif v.split('/')[0] == 'ground':  # change item position
                            new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, S_H)
                        elif v == 'bonus/coin':  # change item position
                            new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, S_H - G_H_S - 152,
                                                         6)
                        elif v == 'bonus/balloon':  # change item position
                            new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, S_H // 2 + 15, 0)
                        elif v.split('/')[0] in ['decor', 'wall_decor', 'star', 'lava']:  # change item position
                            y_pos = S_H - G_H_S - 42
                            if v.split('/')[0] in ['lava']:
                                y_pos = S_H - 5
                            if v.split('/')[0] in ['wall_decor']:
                                y_pos -= 200
                            if v.split('/')[0] in ['star']:
                                if self.area == 2:
                                    y_pos -= 150
                                else:
                                    y_pos -= 300
                            if v == 'wall_decor/candle':
                                new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, y_pos, 9)
                            else:
                                new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, y_pos)
                        else:
                            new_item_class = input_class(f'../src/assets/images/items/{v}.png')  # create item class
                        group_class.add(new_item_class)  # -----------------------  add new class to item_group
                    self.background.distance_mt += 1  # prevent create double sp if player stay in same position

        def distance_counter(*args):
            match int(self.background.distance_mt):
                case 25:
                    Sound.sign_go(self)
                    self.background.distance_mt += 1  # prevent play double sound if player stay in same position
                    # self.state = 'level_statistic'
                case 550:
                    Sound.sign_middle(self)
                    self.background.distance_mt += 1  # prevent ...
                case 1080:  # Finished level
                    self.level_reader_row += 1  # read row level from txt
                    self.background.distance_mt = 0  # prevent ...
                    self.is_music_play = False
                    Sound.stop_all_sounds()
                    Sound.statistic_music(self)
                    self.state = 'level_statistic'  # switch to statistic state

        def area_label():  # Info Table label when Start new Area/Level
            image = pygame.image.load('../src/assets/images/frames/level_frame.png')
            if self.area % 5 != 0 and self.background.distance_mt < 10:
                SCREEN.blit(image, [S_W // 2 - 80, S_H // 2 - 32])
                if self.level < 5:
                    text_creator(f'Level {self.level} - {self.area}', 'white', S_W // 2 - 58, S_H // 2, 36)
                else:
                    text_creator('-FINAL-', 'teal', S_W // 2 - 46, S_H // 2, 36)
            elif self.background.distance_mt == 0:
                SCREEN.blit(image, [S_W // 2 - 80, S_H // 2 - 32])
                text_creator('BONUS', 'yellow', S_W // 2 - 46, S_H // 2, 36)

        # ============================ level manipulator
        if self.area == 11 and self.level < 5:
            self.level += 1
            self.area = 1
        elif self.level == 5:
            self.area = 11
        # ==============---------------level manipulator end

        # ==================== # check is player ALIVE
        if self.player_data.is_player_dead:
            if self.player_data.energy_power < 0:
                self.player_data.energy_power = 0  # set low boundary draw energy bar
            if key_pressed(pygame.K_RIGHT):  # prevent player movie right and finish level after dead
                self.background.distance_mt = -11
            time_now = pygame.time.get_ticks()  # 2sec time delay before go to state 'player_dead'
            if time_now - self.start_timer > self.COOLDOWN:
                self.start_timer = time_now
                self.count_visit += 1
                if self.count_visit == 2:
                    self.player_data.life -= 1
                    Sound.stop_all_sounds()
                    if self.player_data.life > 0:
                        Sound.player_lost_live_music(self)
                        self.state = 'player_dead'
                    if self.player_data.life == 0:
                        Sound.player_dead_funeral_march(self)
                        self.state = 'funeral_agency'  # - Game Over

        # ========================================== START GAME  with Area 1; Level 1 / Wood One
        if self.area == 1:
            if not self.is_start_area:
                # set music
                Sound.forest_music_area_one(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_1.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                self.is_start_area = True

        # ========================================== START GAME  with Area 1; Level 2 / Sea One - Logs
        if self.area == 2:
            if not self.is_start_area:
                # set music
                Sound.sea_music_area_two(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_2.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                # add rock ground
                ground_group.empty()
                ground_rock = Ground('../src/assets/images/ground/dock_middle.png', False, 0, S_H - 75)
                ground_group.add(ground_rock)
                self.is_start_area = True
            self.player_data.jump_limit = S_H - 50  # prevent jump from water
            # check is player in the Sea and allowed animation
            if self.player_data.check_is_player_fail_out_of_screen():
                Sound.player_fail_in_water(self)
                self.is_in_water = True

        # ========================================== START GAME  with Area 1; Level 3 / Volcano
        if self.area == 3:
            if not self.is_start_area:
                # set music
                Sound.volcano_music_area_three(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_3.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                ground_group.empty()
                ground_group.add(ground)
                self.is_start_area = True

        # ========================================== START GAME  with Area 1; Level 4 / Ice
        if self.area == 4:
            if not self.is_start_area:
                # set music
                Sound.ice_music_area_four(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_4.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                # change player friction
                self.player_data.PLAYER_FRICTION = -0.07
                if self.level > 1:
                    FallEffect.snow_list = []  # clear snow/rein list
                    fall_effect_group.add(FallEffect('snow'))
                self.is_start_area = True

        # ==========================================    *** BONUS 1 -  Night Sky*** Level 5
        if self.area == 5:
            if not self.is_start_area:
                self.player_data.is_drive_jeep = True

                # resize image and set background
                if self.level & 1:
                    # set music
                    Sound.bonus_level_one(self)
                    bg_image = '../src/assets/images/backgrounds/bg_level_bonus_1.png'
                else:
                    Sound.bonus_level_one_2(self)
                    fall_effect_group.add(FallEffect('snow', 'white', 2, 2, True))
                    bg_image = '../src/assets/images/backgrounds/bg_level_bonus_1_2.png'
                scaled_img = scale_image(bg_image, 800, 510)
                self.background = Background(scaled_img, 0, 90, False, player.velocity.x, True)

                self.player_data.pos.x = S_W // 2
                self.is_start_area = True

            # fix jeep position
            self.player_data.rect.y += 70
            pic_num = 1

            # change image player if bonus level -------------------------------------------------------
            if key_pressed(pygame.K_UP) or key_pressed(pygame.K_DOWN) or key_pressed(pygame.K_SPACE) \
                    or key_pressed(pygame.K_LEFT) or key_pressed(pygame.K_RIGHT):
                self.player_data.is_bonus_level = True
                pic_num = randrange(1, 4)
            if self.level & 1:
                if key_pressed(pygame.K_LEFT):
                    self.background.distance_mt = 100
                    self.player_data.image = pygame.image.load(f'../src/assets/images/player/jeep/jeep_sp/{pic_num}.png')
                elif key_pressed(pygame.K_RIGHT):
                    self.background.distance_mt = 100
                    flipped_pic = pygame.transform.\
                        flip(pygame.image.load(f'../src/assets/images/player/jeep/jeep_sp/{pic_num}.png'), True, False)
                    self.player_data.image = flipped_pic
                else:
                    if self.player_data.direction.x == -1:
                        self.player_data.image = pygame.image.load('../src/assets/images/player/jeep/1.png')
                    else:
                        self.player_data.image = pygame.image.load('../src/assets/images/player/jeep/2.png')
            else:
                if key_pressed(pygame.K_RIGHT):
                    self.background.distance_mt = 100
                    self.player_data.image = pygame.image.load('../src/assets/images/player/sled/1.png')
                elif key_pressed(pygame.K_LEFT):
                    self.player_data.image = pygame.image.load('../src/assets/images/player/sled/2.png')
                else:
                    if self.player_data.direction.x == 1:
                        self.player_data.image = pygame.image.load('../src/assets/images/player/sled/1.png')
                    else:
                        self.player_data.image = pygame.image.load('../src/assets/images/player/sled/2.png')
            # -----------------  create and add bonus to group
            time_now = pygame.time.get_ticks()
            if time_now - self.start_timer > self.COOLDOWN:
                self.start_timer = time_now
                if self.count_visit == randrange(1, 21):  # create bomb if random num match
                    bonus_group.add(Bonus('../src/assets/images/items/bonus/comet.png'))
                else:
                    bonus_group.add(Bonus('../src/assets/images/items/bonus/star_small.png'))
                self.count_visit += 1
            if self.count_visit == 21 or self.player_data.is_player_dead:
                self.count_visit = 0
                self.level_reader_row += 1  # read row level from txt
                self.background.distance_mt = 0  # prevent ...
                self.is_music_play = False
                Sound.stop_all_sounds()
                Sound.statistic_music(self)
                self.state = 'level_statistic'

        # ========================================== START GAME  with Area 1; Level 6 / Wood Two - Dark
        if self.area == 6:
            if not self.is_start_area:
                # set music
                Sound.dark_forest_music_area_five(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_5.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                if not self.level & 1:  # make rain
                    FallEffect.snow_list = []  # clear snow/rein list
                    fall_effect_group.add(FallEffect('rein', 'aqua'))
                self.is_start_area = True

        # ========================================== START GAME  with Area 1; Level 7 / Sea Two - Clouds
        if self.area == 7:
            if not self.is_start_area:
                # set music
                self.current_music = Sound.sea_two_music_area_six(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_6.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True,)
                # add rock ground
                ground_group.empty()
                ground_rock = Ground('../src/assets/images/ground/dock_sea.png', False, 0, S_H - 200)
                ground_group.add(ground_rock)
                self.is_start_area = True
            # check is player in the Sea and allowed animation
            if self.player_data.check_is_player_fail_out_of_screen():
                Sound.player_fail_in_water(self)
                self.is_in_water = True
            # prevent squat player in could level
            self.player_data.is_water_level = True

        # ========================================== START GAME  with Area 1; Level 8 / Desert
        if self.area == 8:
            if not self.is_start_area:
                # set music
                self.current_music = Sound.desert_music_area_seven(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_7.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                ground_group.empty()
                ground_group.add(ground)
                self.is_start_area = True

        # ========================================== START GAME  with Area 1; Level 9 /Front of the castle
        if self.area == 9:
            if not self.is_start_area:
                # set music
                Sound.front_castle_music_area_eight(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_8.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                self.is_start_area = True

        # ==========================================    *** BONUS 2 - Buy Yacht***  Level 10
        if self.area == 10:
            if not self.is_start_area:
                self.player_data.is_drive_jeep = False
                # set music
                Sound.bonus_level(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_bonus_2.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, False, player.velocity.x, True)
                self.player_data.image = pygame.image.load('../src/assets/images/player/boat/1.png')
                self.is_start_area = True

            # change image player if bonus level -------------------------------------------------------
            if key_pressed(pygame.K_UP) or key_pressed(pygame.K_DOWN) or key_pressed(pygame.K_SPACE)\
                    or key_pressed(pygame.K_LEFT) or key_pressed(pygame.K_RIGHT):
                self.player_data.is_bonus_level = True

            if key_pressed(pygame.K_LEFT):
                self.background.distance_mt = 100
                self.player_data.image = pygame.image.load('../src/assets/images/player/boat/1.png')
            elif key_pressed(pygame.K_RIGHT):
                self.player_data.image = pygame.image.load('../src/assets/images/player/boat/2.png')
                self.background.distance_mt = 100
            else:
                if self.player_data.direction.x == -1:
                    self.player_data.image = pygame.image.load('../src/assets/images/player/boat/1.png')
                else:
                    self.player_data.image = pygame.image.load('../src/assets/images/player/boat/2.png')

            # -----------------  create and add bonus to group
            time_now = pygame.time.get_ticks()
            if time_now - self.start_timer > self.COOLDOWN:
                self.start_timer = time_now
                if self.count_visit == randrange(1, 21):  # create bomb if random num match
                    bonus_group.add(Bonus('../src/assets/images/items/bonus/bomb.png'))
                else:
                    bonus_group.add(Bonus())
                self.count_visit += 1
            if self.count_visit == 21 or self.player_data.is_player_dead:
                self.count_visit = 0
                self.level_reader_row += 1  # read row level from txt
                self.background.distance_mt = 0  # prevent ...
                self.is_music_play = False
                Sound.stop_all_sounds()
                Sound.statistic_music(self)
                self.state = 'level_statistic'

        # ========================================== START GAME  with Area 10;Level 11 / Castle FINAL /***BOSS***
        if self.area == 11:
            if self.is_start_area:
                Sound.stop_all_sounds()
                if self.level_reader_row == 41:  # read from row 41
                    # set music
                    self.current_music = Sound.in_the_castle_music_area_final(self)
                    # resize image and set background
                    scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_10_1.png', 800, 510)
                    self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                elif self.level_reader_row == 42:  # read from row 42
                    # set music
                    self.current_music = Sound.in_the_castle_music_area_final_two(self)
                    # resize image and set background
                    scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_10_2.png', 800, 510)
                    self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                    ground_group.empty()
                    ground_rock = Ground('../src/assets/images/ground/stone_platform.png', False, 0, S_H - 62)
                    ground_group.add(ground_rock)
                    self.player_data.jump_limit = S_H - 50  # prevent jump from water
                elif self.level_reader_row == 43:  # read from row 43
                    # set music
                    self.current_music = Sound.in_the_castle_music_area_final_three(self)
                    # resize image and set background
                    scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_10_3.png', 800, 510)
                    self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                    ground_group.empty()
                    ground_group.add(ground)
                elif self.level_reader_row == 44:  # read from row 44  The BOSS
                    self.state = 'boss'
                    return
                self.is_start_area = False
            # check is player in the Lava and allowed animation
            if self.player_data.check_is_player_fail_out_of_screen():
                Sound.player_fail_in_water(self)
                self.is_in_water = True

        # =================== check is player energy player/ dead - and set image
        if self.player_data.check_is_energy_player():
            [asg[group].empty() for group in asg if group != 'ground' and group != 'player']  # remove item/enemy
            self.player_data.rect.center = [self.player_data.player_dead_x_pos, S_H - G_H_S + 10]
            pic = self.player_data.image = pygame.image.load('../src/assets/images/player/dead/dead.png')
            SCREEN.blit(pic, [self.player_data.player_dead_x_pos, S_H - GROUND_HEIGHT_SIZE + 10])

        # ============== create level: items, enemy, and more
        items_dict = eval(file_operation('levels/levels_data.txt', 'r', self.level_reader_row))
        sprite_creator(items_dict, Item, item_group)

        # ============= level counter
        distance_counter()

        # =================================================== UPDATE
        # update BG
        self.background.update()
        # --------------------------- draw sprite group
        if self.area == 2 or self.area == 7 or (self.area == 11 and self.level_reader_row == 42):
            ground_group.draw(SCREEN)  # hide under bg or removed
            if self.is_in_water:  # run splashes animation
                if self.level < 5:
                    pic = pygame.image.load('../src/assets/images/splashes/splashes.png')
                else:
                    pic = pygame.image.load('../src/assets/images/splashes/splashes_fire.png')
                self.count += 0.03
                pic = pygame.transform.rotozoom(pic, 0, self.count)
                pos = pic.get_rect(center=(self.player_data.player_dead_x_pos, S_H - 100))
                SCREEN.blit(pic, pos)
        item_group.draw(SCREEN)
        player_group.draw(SCREEN)
        bullets_group.draw(SCREEN)
        bonus_group.draw(SCREEN)
        fall_effect_group.draw(SCREEN)
        # --------------------------- update sprite group
        ground_group.update()
        player_group.update()
        bullets_group.update()
        item_group.update()
        bonus_group.update()
        fall_effect_group.update()
        # ============== draw current area/level labels
        area_label()

    def boss(self):
        player.is_boss_level = True  # set player walking border to all SCREEN_WIDTH
        # top display frames
        table.update()
        if self.boss_number == 1:
            text_creator(f'FPS {int(CLOCK.get_fps())}', 'white', 10, 10, 25)

            if not self.is_bg_created:
                Sound.stop_all_sounds()
                Sound.boss_battle_final(self)
                # resize image
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_10_4.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, False, player.velocity.x, True)
            self.is_bg_created = True

            if self.knight_data.is_dead and self.is_start_area:
                self.is_start_area = False
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_10_4_1.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, False, player.velocity.x, True)

            if self.player_data.is_player_kill_boss:
                self.is_visited = False
                self.state = 'level_statistic'
            if self.player_data.is_player_dead:
                self.state = 'player_dead'

            # # # =================================================== UPDATE
            # update BG
            self.background.update()
            # # # --------------------------- draw sprite group
            bullets_group.draw(SCREEN)
            player_group.draw(SCREEN)
            knight_group.draw(SCREEN)
            # # # --------------------------- update sprite group
            player_group.update()
            knight_group.update()
            bullets_group.update()

    def intro(self, ):
        Intro()
        Intro.event(self)

    def menu(self):
        Menu()
        Menu.event(self)

    def story(self):
        Story()
        Story.event(self)

    def score(self):
        background_image('../src/assets/images/backgrounds/bg_score.png')
        text_creator('TOP RANKING LIST', 'orange', SCREEN_WIDTH // 2 - 140, 100, 40, None, None, True)
        if not self.ranking_list:
            text_creator('No Internet!', 'red3', 300, S_H // 2 - 50, 50)
            text_creator('or', 'peachpuff', 380, S_H // 2, 40)
            text_creator('Requests operation failed...', 'cadetblue4', 170, S_H // 2 + 50, 50)
        for i in range(len(self.ranking_list)):
            name, score = self.ranking_list[i]
            if i < 3:
                color = 'brown3'
            elif i & 1:
                color = 'grey'
            else:
                color = 'olivedrab'
            text_creator(f'{i + 1})   {score} ', color, SCREEN_WIDTH // 2 - 130, 150 + i * 40, 30)
            text_creator('-', color, SCREEN_WIDTH // 2 + 10, 150 + i * 40, 30)
            text_creator(f'{name}', color, SCREEN_WIDTH // 2 + 50, 150 + i * 40, 30)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Sound.btn_click(self)
                    self.state = 'menu'
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def write_score(self):

        background_image('../src/assets/images/backgrounds/bg_write_score.png')
        text_creator(self.input_text, 'teal', 315, SCREEN_HEIGHT - 110, 32)
        pygame.draw.rect(SCREEN, 'white', pygame.Rect((310, 470, 175, 40)), 2, 2)

        exit_game()
        if key_pressed(pygame.K_RETURN):
            Sound.btn_click(self)
            post(self.input_text, self.player_data.points)
            self.ranking_list.append((self.input_text, self.player_data.points))
            self.ranking_list = sorted(self.ranking_list, key=lambda x: x[1], reverse=True)[:-1]
            pygame.time.delay(100)
            self.state = 'score'
        if key_pressed(pygame.K_BACKSPACE):
            self.input_text = ''

        keys = pygame.key.get_pressed()
        for i in range(pygame.K_a, pygame.K_z + 1):
            if keys[i]:
                if len(self.input_text) < 10:
                    time_now = pygame.time.get_ticks()
                    if time_now - self.start_timer > 150:
                        self.start_timer = time_now
                        self.input_text += pygame.key.name(i)
                        self.input_text = self.input_text.title()

    def epilogue(self):
        self.is_start_new_game = True  # old game finish
        Epilogue(self.player_data, self.ranking_list)
        Epilogue.event(self)

    def player_dead(self):
        if self.player_data.life <= 0:
            Sound.stop_all_sounds()
            Sound.player_dead_funeral_march(self)
            self.state = 'funeral_agency'
        # ====================================== reset part of game_state data
        self.is_start_area = False
        if self.level == 5:
            self.is_start_area = True
            self.is_bg_created = False
        self.is_in_water = False
        self.background = None
        self.count = 0
        self.count_visit = 0
        # clear all group --------------
        [all_spite_groups_dict[group].empty() for group in all_spite_groups_dict if group != 'ground']
        all_spite_groups_dict['player'].add(player)
        all_spite_groups_dict['knight'].add(knight)
        self.player_data.reset_current_player_data()  # reset player data for current game
        self.knight_data.reset_knife_data()  # reset boss data for current game

        # -------------------------------------- go to state
        PlayerDead(self.player_data, self.area, self.level)
        PlayerDead.event(self)
        # print(4)

    def funeral_agency(self):
        background_image('../src/assets/images/backgrounds/bg_funeral_agency.png', 0, 0)
        text_creator('Press BACKSPACE to continue...', 'cornsilk', S_W - 280, S_H - 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.is_start_new_game = True  # for reset old game
                    Sound.stop_all_sounds()
                    self.ranking_list = ranking_manipulator()
                    if self.ranking_list:
                        if self.ranking_list[9][1] <= self.player_data.points:
                            self.state = 'write_score'
                            return
                    self.state = 'intro'

    def level_statistic(self):
        # reset part of game state
        if self.level < 5:
            self.is_start_area = False
        else:
            self.is_start_area = True

        self.player_data.is_water_level = False
        # self.player_data.is_bonus_level = False
        self.background = None
        self.player_data.PLAYER_FRICTION = -0.12
        self.player_data.WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH // 3
        [asg[group].empty() for group in asg if group not in ['ground', 'player', 'knight']]  # remove all
        # ---------------------------------------------
        table.update()

        if screen_transition_animation() >= 0:  # clear screen
            LevelStatistic(self.bonus_pts, self.player_data, self.level, self.area, self.amulets_counter).update()
            LevelStatistic(self.bonus_pts, self.player_data, self.level, self.area, self.amulets_counter).event(self)

            if self.player_data.is_bonus_level and not self.is_add_bonus:  # for bonus level
                if player.bonus_coins:
                    player.points += 1000 * player.bonus_coins
                player.points += 5000
                self.is_add_bonus = True
            elif self.player_data.is_player_kill_boss and not self.is_add_bonus:  # BOSS WAS KILLED
                self.amulets_counter = 9
                player.points += self.player_data.life * 10_000
                player.points += 50_000
                Sound.add_point_two(self)
                self.is_add_bonus = True
            elif self.player_data.energy_power > 0 and not self.is_add_bonus:  # add bonus points to score
                Sound.add_point(self)
                self.player_data.energy_power -= 1
                self.bonus_pts += 30  # 3000 pts
                player.points += round(self.player_data.energy_power % 10 + 25.5)
                if self.bonus_pts >= 3000:
                    if not self.is_visited:
                        Sound.voice_perfect(self)
                        self.is_visited = True
                    self.player_data.points += 5000
            elif not self.is_add_bonus and player.energy_power == 0 and \
                    (player.bonus_coins or player.bonus_statuette or player.is_player_kill_boss):
                Sound.grab_coin(self)
                if player.bonus_coins:
                    player.points += 1000 * player.bonus_coins
                if player.bonus_statuette:
                    player.points += 3000
                if player.is_player_kill_boss:
                    player.points += 5000
                self.is_add_bonus = True

    def start_pause(self):
        table.update()
        background_image('../src/assets/images/pause/bg_toilet.png', 50, 100)
        text_creator('PAUSED', 'chocolate1', S_W // 2 - 50, S_H // 2, 40, None, None, True)
        text_creator('Press RETURN to continue...', 'cornsilk', S_W - 250, S_H - 30)

        time_now = pygame.time.get_ticks()
        if time_now - self.start_timer > self.COOLDOWN:
            self.start_timer = time_now
            bonus_group.add(Bonus('../src/assets/images/pause/toilet_roll/roll.png'))
        bonus_group.draw(SCREEN)
        bonus_group.update()

        if key_pressed(pygame.K_RETURN):
            Sound.btn_click(self)
            self.state = 'start_game'
            bonus_group.empty()

    def real_time_statistics(self):
        background_image('../src/assets/images/backgrounds/bg_EMPTY.png')
        if self.level_reader_row < 44:
            text_creator('REAL TIME STATISTICS', 'slateblue3', S_W // 2 - 160, 40, 40, None, None, True)
        else:
            self.is_final_statistics = True
            text_creator('GENERAL STATISTICS', 'slateblue3', S_W // 2 - 160, 40, 40, None, None, True)
        text_creator('Press RETURN to continue...', 'cornsilk', S_W - 250, S_H - 14)

        if not self.is_visited:
            sort_by_keys = sorted(self.player_data.statistics.items(), key=lambda keys: keys)
            sort_by_values = {k: sorted(v.items(), key=lambda v: -v[1]) for k, v in sort_by_keys}

            for key, val in sort_by_values.items():
                # print(key)
                for k, v in val:
                    self.col_counter += 1
                    if self.col_counter % 12 == 0:
                        self.gen_row_spacer += 100
                        self.gen_col_spacer = 0
                    # print({key: {k, v}})
                    self.current_list.append([key, k, v, self.gen_row_spacer, self.gen_col_spacer])
                    self.gen_col_spacer += 40
            self.is_visited = True

        for key, k, v, row, col in self.current_list:
            if key != 'enemies':
                if key == 'trap':
                    k = '1'
                img = pygame.image.load(f'../src/assets/images/items/{key}/{k}.png')
            else:
                img = pygame.image.load(f'../src/assets/images/{key}/{k}/1.png')

            scaled_img = pygame.transform.scale(img, (25, 25))
            SCREEN.blit(scaled_img, (10 + row, 90 + col))
            text_creator(f' = {v}', 'sienna1', 40 + row, 105 + col, 30)

        if key_pressed(pygame.K_RETURN) and not self.is_final_statistics:
            self.current_list = []
            self.gen_col_spacer = 0
            self.gen_row_spacer = 0
            self.col_counter = -1
            self.is_visited = False
            Sound.btn_click(self)
            self.state = 'start_game'
        if key_pressed(pygame.K_RETURN) and self.is_final_statistics:
            Sound.stop_all_sounds()
            Sound.score_music(self)
            if self.ranking_list:
                if self.player_data.points >= self.ranking_list[9][1]:
                    self.state = 'write_score'
                    return
            self.state = 'score'

    def credits(self):
        background_image('../src/assets/images/backgrounds/bg_EMPTY.png')
        text_creator('CREDITS', 'slateblue3', S_W // 2 - 60, 40, 40, None, None, True)
        text_creator('version: 1.0.0-beta', 'cornsilk', S_W - 130, 20, 20)

        text_creator('Free images:', 'brown', 110, 100, 35)
        text_creator('https://www.pngwing.com', 'cadetblue4', 130, 125, 30)
        text_creator('https://www.freepik.com', 'cadetblue4', 130, 145, 30)
        text_creator('https://craftpix.net', 'cadetblue4', 130, 165, 30)

        text_creator('Free sounds:', 'brown', 110, 200, 35)
        text_creator('https://freesound.org/', 'cadetblue4', 130, 225, 30)
        text_creator('https://pixabay.com/', 'cadetblue4', 130, 245, 30)
        text_creator('https://orangefreesounds.com', 'cadetblue4', 130, 265, 30)

        text_creator('Platform 2D game:', 'brown', 110, S_H // 2, 34)
        text_creator('https://www.pygame.org', 'cadetblue4', 130, S_H // 2 + 24, 30)

        SCREEN.blit(pygame.image.load('../src/assets/images/title_icon/pygame_logo.png'), (S_W // 4 - 50, S_H - 266))

        text_creator('Developer:', 'brown', 30, S_H - 55, 30)
        text_creator('by Abaddon', 'cadetblue4', 50, S_H - 35, 30)

        text_creator('Bug rapports:', 'brown', S_W // 2 - 90, S_H - 55, 30)
        text_creator('subtotal@abv.bg', 'cadetblue4', S_W // 2 - 70, S_H - 35, 30)

        text_creator('Copyright:', 'brown', S_W - 140, S_H - 55, 30)
        text_creator('© 2023', 'cadetblue4', S_W - 120, S_H - 35, 30)

        text_creator('Press RETURN to continue...', 'cornsilk', S_W - 240, S_H - 10, 24)

        if key_pressed(pygame.K_RETURN):
            Sound.btn_click(self)
            self.state = 'start_game'
            bonus_group.empty()

    # ========================================= state manager
    def state_manager(self):
        # print(self.state)
        if self.state == 'pause':
            self.start_pause()
        if self.state == 'intro':
            self.intro()
        if self.state == 'menu':
            self.menu()
        if self.state == 'story':
            self.story()
        if self.state == 'score':
            self.score()
        if self.state == 'start_game':
            self.start_game()
        if self.state == 'level_statistic':
            self.level_statistic()
        if self.state == 'boss':
            self.boss()
        if self.state == 'player_dead':
            self.player_dead()
        if self.state == 'funeral_agency':
            self.funeral_agency()
        if self.state == 'epilogue':
            self.epilogue()
        if self.state == 'write_score':
            self.write_score()
        if self.state == 'real_time_statistics':
            self.real_time_statistics()
        if self.state == 'credits':
            self.credits()


#  ================================ create new GameState
game_state = GameState(player, knight, background)

# ================================================================ create top Table for: score , energy and more
table = Table(game_state, player, knight)

# ============= Starting Game loop
while True:
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(FPS)
    exit_game()
