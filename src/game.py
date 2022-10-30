from settings import *
from classes.class_background import Background
from classes.class_table import Table
from src.classes.class_sound import Sound
from state_classes import Intro, Menu, Legend, Score, LevelStatistic, PlayerDead
from classes.class_player import Player
from classes.class_knight import Knight
from classes.class_ground import Ground
from classes.class_bullet import Bullet
from classes.class_item import Item
from classes.class_enemy import Enemy
from classes.class_cloud import Cloud
from classes.class_log import Log
from classes.class_bonus import Bonus

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

# add to all_sprite_groups   /items group included enemy/
all_spite_groups_dict = {'player': player_group, 'knight': knight_group, 'bullets': bullets_group,
                         'ground': ground_group, 'items': item_group, 'bonus': bonus_group}

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
    start_timer = pygame.time.get_ticks()
    count_visit = 0

    def __init__(self, player_data, knight_data, background_data):
        self.state = 'intro'
        self.current_music = Sound.intro_music(self)
        self.is_music_play = False
        self.background = None
        self.is_bg_created = False
        self.area = 1
        self.level = 5
        self.boss_number = 1
        self.level_reader_row = 28 # 1
        self.player_data = player_data
        self.knight_data = knight_data
        self.background_data = background_data
        self.bonus_pts = 0
        self.is_add_bonus = False
        self.is_start_new_game = False
        self.is_in_water = False
        self.is_star_area = False
        self.count = 0

    def start_game(self):
        # ------------------top display frame
        table.update()

        # =============================================== RESET ALL DATA IF START NEW GAME
        if self.is_start_new_game:  # reset all old data
            self.is_start_new_game = False
            Sound.stop_all_sounds()
            self.player_data.reset_all_player_data_for_new_game()  # reset all player data
            [all_spite_groups_dict[group].empty() for group in all_spite_groups_dict]
            all_spite_groups_dict['player'].add(player)
            all_spite_groups_dict['knight'].add(knight)
            all_spite_groups_dict['ground'].add(ground)
            self.level = 1
            self.area = 1
            self.boss_number = 1
            self.level_reader_row = 1
            self.bonus_pts = 0
            self.count = 0
            self.is_add_bonus = False
            self.is_in_water = False
            self.background = None
            self.is_star_area = False
            self.player_data.is_water_level = False
        # -----------------------------------------------
        self.bonus_pts = 0  # reset pts
        player.is_boss_level = False  # set player walking border to 1/3 S_W
        # player.is_bonus_level = False

        # ++++++++++++++++++++++++++++++ developer utils +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        text_creator(f'FPS {int(CLOCK.get_fps())}', 'white', 10, 5, 25)
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
            if enemy_name == 'enemy_knight_sword':
                return Enemy(Bullet, asg, background, '../src/assets/images/enemies/knight_sword/1.png',
                             S_W, S_H - G_H_S - 55, 0, True, False, None, None, 8, True)

        # ================================ create cloud platform classes
        def platform_creator(v_type):

            if v_type == 'cloud/small' or v_type ==   'cloud/small_low' :
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
                            # test move to decoration !!!!!!!!!!
                            new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, 250)
                        elif v.split('/')[0] == 'ground':  # change item position
                            new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, S_H)
                        elif v == 'bonus/coin':  # change item position
                            new_item_class = input_class(f'../src/assets/images/items/{v}.png', S_W, S_H - G_H_S - 152,
                                                         6)
                        elif v == 'bonus/balloon':  # change item position
                            # test move to decoration !!!!!!!!!!
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
                    # self.state = 'level_statistic'
                    self.background.distance_mt += 1  # prevent play double sound if player stay in same position
                case 550:
                    Sound.sign_middle(self)
                    self.background.distance_mt += 1  # prevent ...
                case 1080:  # Finished level
                    Sound.sign_finish(self)
                    self.level_reader_row += 1  # read row level from txt
                    self.background.distance_mt = 0  # prevent ...
                    self.is_music_play = False
                    Sound.stop_all_sounds()
                    Sound.statistic_music(self)
                    self.state = 'level_statistic'  # switch to statistic state

        def area_label():  # Info Table label when Start new Area/Level
            if self.area != 9 and self.background.distance_mt < 10:
                image = pygame.image.load('../src/assets/images/frames/level_frame.png')
                SCREEN.blit(image, [S_W // 2 - 80, S_H // 2 - 32])
                text_creator(f'Level {self.level} - {self.area}', 'white', S_W // 2 - 58, S_H // 2, 36)
            if self.area == 9 and self.background.distance_mt == 0:
                image = pygame.image.load('../src/assets/images/frames/level_frame.png')
                SCREEN.blit(image, [S_W // 2 - 80, S_H // 2 - 32])
                text_creator('BONUS', 'yellow', S_W // 2 - 46, S_H // 2, 36)

        # ============================ level manipulator
        if self.area == 10 and self.level < 9:
            self.level += 1
            self.area = 1

        # if self.area > 9:
        #     if self.knight_data.is_boss_level_complete:
        #         self.area = 1
        #         self.level += 1
        #

        # ==============---------------level manipulator end

        # ==================== # check is player ALIVE
        if self.player_data.is_player_dead:
            self.background_data.is_allowed_move = False  # stop move background if key pressed
            time_now = pygame.time.get_ticks()  # 2sec time delay before go to state 'player_dead'
            if time_now - self.start_timer > self.COOLDOWN:
                self.start_timer = time_now
                print(3)
                self.count_visit += 1
                if self.count_visit == 2:
                    self.background_data.is_allowed_move = True  # restore move background if key pressed
                    self.player_data.lives -= 1
                    Sound.stop_all_sounds()
                    if self.player_data.lives > 0:
                        Sound.player_lost_live_music(self)
                        self.state = 'player_dead'
                    if self.player_data.lives == 0:
                        Sound.player_dead_funeral_march(self)
                        self.state = 'funeral_agency'  # - Game Over

        # ========================================== START GAME  with Area 1; Level 1 / Wood One
        if self.area == 1:
            if not self.is_star_area:
                # set music
                Sound.forest_music_area_one(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_1.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                self.is_star_area = True

        # ========================================== START GAME  with Area 1; Level 2 / Sea One - Logs
        if self.area == 2:
            if not self.is_star_area:
                # set music
                Sound.sea_music_area_two(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_2.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                # add rock ground
                ground_group.empty()
                ground_rock = Ground('../src/assets/images/ground/dock_middle.png', False, 0, S_H - 75)
                ground_group.add(ground_rock)
                self.is_star_area = True
            self.player_data.jump_limit = S_H - 50  # prevent jump from water
            # check is player in the Sea and allowed animation
            if self.player_data.check_is_player_fail_out_of_screen():
                Sound.player_fail_in_water(self)
                self.is_in_water = True

        # ========================================== START GAME  with Area 1; Level 3 / Volcano
        if self.area == 3:
            if not self.is_star_area:
                # set music
                Sound.volcano_music_area_three(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_3.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                ground_group.empty()
                ground_group.add(ground)
                self.is_star_area = True

        # ========================================== START GAME  with Area 1; Level 4 / Ice
        if self.area == 4:
            if not self.is_star_area:
                # set music
                Sound.ice_music_area_four(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_4.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                # change player friction
                self.player_data.PLAYER_FRICTION = -0.07
                self.is_star_area = True

        # ========================================== START GAME  with Area 1; Level 5 / Wood Two - Dark
        if self.area == 5:
            if not self.is_star_area:
                # set music
                Sound.dark_forest_music_area_five(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_5.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                self.is_star_area = True

        # ========================================== START GAME  with Area 1; Level 6 / Sea Two - Clouds
        if self.area == 6:
            if not self.is_star_area:
                # set music
                self.current_music = Sound.sea_two_music_area_six(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_6.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True,)
                # add rock ground
                ground_group.empty()
                ground_rock = Ground('../src/assets/images/ground/dock_sea.png', False, 0, S_H - 200)
                ground_group.add(ground_rock)
                self.is_star_area = True
            # check is player in the Sea and allowed animation
            if self.player_data.check_is_player_fail_out_of_screen():
                Sound.player_fail_in_water(self)
                self.is_in_water = True
            # prevent squat player in could level
            self.player_data.is_water_level = True

        # ========================================== START GAME  with Area 1; Level 7 / Desert
        if self.area == 7:
            if not self.is_star_area:
                # set music
                self.current_music = Sound.desert_music_area_seven(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_7.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                ground_group.empty()
                ground_group.add(ground)
                self.is_star_area = True

        # ========================================== START GAME  with Area 1; Level 8 /Front of the castle
        if self.area == 8:
            if not self.is_star_area:
                # set music
                Sound.front_castle_music_area_eight(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_8.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                self.is_star_area = True

        # ==========================================    *** BONUS ***
        if self.area == 9:
            if not self.is_star_area:
                # set music
                Sound.bonus_level(self)
                # resize image and set background
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_bonus.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, False, player.velocity.x, True)
                self.player_data.image = pygame.image.load('../src/assets/images/player/boat/y1.png')
                self.is_star_area = True

            # change image player if bonus level -------------------------------------------------------
            if key_pressed(pygame.K_UP) or key_pressed(pygame.K_DOWN) or key_pressed(pygame.K_SPACE)\
                    or key_pressed(pygame.K_LEFT) or key_pressed(pygame.K_RIGHT):
                self.player_data.is_bonus_level = True

            if key_pressed(pygame.K_LEFT):
                self.background.distance_mt = 100
                self.player_data.image = pygame.image.load('../src/assets/images/player/boat/y1.png')
            elif key_pressed(pygame.K_RIGHT):
                self.player_data.image = pygame.image.load('../src/assets/images/player/boat/y2.png')
                self.background.distance_mt = 100
            else:
                if self.player_data.direction.x == -1:
                    self.player_data.image = pygame.image.load('../src/assets/images/player/boat/y1.png')
                else:
                    self.player_data.image = pygame.image.load('../src/assets/images/player/boat/y2.png')
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

        # ========================================== START GAME  with Area 10;Level 9 / Castle FINAL
        if self.area == 10:
            if not self.is_star_area:
                if self.level_reader_row == 15:  # 57
                    # set music
                    self.current_music = Sound.in_the_castle_music_area_then(self)
                    # resize image and set background
                    scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_10_1.png', 800, 510)
                    self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                elif self.level_reader_row == 16:  # 58
                    # set music
                    self.current_music = Sound.in_the_castle_music_area_then_two(self)
                    # resize image and set background
                    scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_10_2.png', 800, 510)
                    self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                    ground_group.empty()
                    ground_rock = Ground('../src/assets/images/ground/stone_platform.png', False, 0, S_H - 62)
                    ground_group.add(ground_rock)
                    self.player_data.jump_limit = S_H - 50  # prevent jump from water
                self.is_star_area = True
            # check is player in the Lava and allowed animation
            if self.player_data.check_is_player_fail_out_of_screen():
                Sound.player_fail_in_water(self)
                self.is_in_water = True

        # ========================================== START GAME  with Area 10;Level  ***BOSS***
        if self.area == 11:
            self.state = 'boss'
            return

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
        if self.area == 2 or self.area == 6 or (self.area == 10 and self.level_reader_row == 11):  # 58
            ground_group.draw(SCREEN)  # hide under bg or removed
            if self.is_in_water:  # run splashes animation
                if self.area < 10:
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
        # --------------------------- update sprite group
        ground_group.update()
        player_group.update()
        bullets_group.update()
        item_group.update()
        bonus_group.update()

        # ============== draw current area/level labels
        area_label()

    def boss(self):
        player.is_boss_level = True  # set player walking border to all SCREEN_WIDTH
        # top display frames
        table.update()
        if self.boss_number == 1:
            text_creator(f'FPS {int(CLOCK.get_fps())}', 'white', 10, 10, 25)
            if not self.is_music_play:
                Sound.stop_all_sounds()
                Sound.boss_music_area_one(self)
                self.is_music_play = True

            if not self.is_bg_created:  # todo remove not  only for test
                # resize image
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_boss/bg_area_one_forest_boss.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, False, player.velocity.x, True)
                self.is_bg_created = True  # todo must be False

            if self.player_data.is_player_kill_boss:
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

    def legend(self):
        Legend()
        Legend.event(self)

    def score(self):
        Score()
        Score.event(self)

    def player_dead(self):
        if self.player_data.lives <= 0:
            Sound.stop_all_sounds()
            Sound.player_dead_funeral_march(self)
            self.state = 'funeral_agency'
        # ====================================== reset part of game_state data
        self.is_star_area = False
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
        print(4)

    def funeral_agency(self):
        background_image('../src/assets/images/player/dead/bg/rip.png', 0, 0)
        if key_pressed(pygame.K_RETURN):
            self.is_start_new_game = True  # for reset old game
            Sound.stop_all_sounds()
            self.state = 'intro'

    def level_statistic(self):
        # reset part of game state
        self.player_data.is_water_level = False
        self.is_star_area = False
        self.background = None
        self.player_data.PLAYER_FRICTION = -0.12
        self.player_data.WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH // 3
        [asg[group].empty() for group in asg if group not in ['ground', 'player', 'knight']]  # remove all
        # ---------------------------------------------
        table.update()

        if screen_transition_animation() >= 0:  # clear screen
            LevelStatistic(self.bonus_pts, self.player_data, self.level).update()
            LevelStatistic(self.bonus_pts, self.player_data, self.level).event(self)

            if self.player_data.is_bonus_level and not self.is_add_bonus:  # for bonus level
                if player.bonus_coins:
                    player.points += 1000 * player.bonus_coins
                player.points += 5000
                self.is_add_bonus = True
            elif self.player_data.energy_power > 0 and not self.is_add_bonus:  # add bonus points to score
                Sound.add_point(self)
                self.player_data.energy_power -= 1
                self.bonus_pts += 30  # 3000 pts
                player.points += round(self.player_data.energy_power % 10 + 25.5)
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

    # ========================================= state manager
    def state_manager(self):
        # print(self.state)
        if self.state == 'intro':
            self.intro()
        if self.state == 'menu':
            self.menu()
        if self.state == 'legend':
            self.legend()
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


#  ================================ create new GameState
game_state = GameState(player, knight, background)

# ================================================================ create top Table for: score , energy and more
table = Table(game_state, player, knight)

# ============= Starting Game loo
while True:
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(FPS)
    exit_game()
