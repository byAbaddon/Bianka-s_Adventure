from settings import *
from classes.class_background import Background
from classes.class_table import Table
from src.classes.class_sound import Sound
from state_classes import Intro, Menu, Legend, Score, LevelStatistic
from classes.class_player import Player
from classes.class_ground import Ground
from classes.class_bullet import Bullet
from classes.class_item import Item
from classes.class_enemy import Enemy

# ================================================================= TEST imported classes
# print(dir(Menu))

# ========================================================================== variables

# ======================================================================== create Sprite groups
background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

# add to all_sprite_groups   /items group include enemy/
all_spite_groups_dict = {'player': player_group, 'bullets': bullets_group, 'ground': ground_group,
                         'items': item_group}

# ======================================================================= initialize  Classes

player = Player(Bullet, all_spite_groups_dict)
ground = Ground()

# ---------------------------------------------------------------------- create Enemies

# variables
pic_monkey = '../src/assets/images/enemies/monkey/monkey.png'
pic_hedgehog = '../src/assets/images/enemies/hedgehog/hedgehog.png'
pic_raven = '../src/assets/images/enemies/raven/1.png'
pic_raven_bullet = '../src/assets/images/bullets/egg.png'
pic_monkey_bullet = '../src/assets/images/bullets/coconut.png'
asg = all_spite_groups_dict

# create enemy classes
enemy_monkey = Enemy(Bullet, asg, pic_monkey, SCREEN_WIDTH, 150, 5, True, True,pic_monkey_bullet, 0.6)

enemy_hedgehog = Enemy(Bullet, asg, pic_hedgehog, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - 5, 1)
enemy_static_hedgehog = Enemy(Bullet, asg, pic_hedgehog, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - 5, 0)

enemy_raven = Enemy(Bullet, asg, pic_raven, SCREEN_WIDTH, TOP_FRAME_SIZE + 100, 3, True, True, pic_raven_bullet, 1, 5)

enemy_classes_dict = {'enemy_monkey': enemy_monkey, 'enemy_hedgehog': enemy_hedgehog, 'enemy_raven': enemy_raven,
                      'enemy_static_hedgehog': enemy_static_hedgehog}

# add to group
# ground2 = Ground('../src/assets/images/ground/distance.png', 100, SCREEN_HEIGHT - 150)
# ground3 = Ground('../src/assets/images/ground/distance.png', 400, SCREEN_HEIGHT - 170)
player_group.add(player)
ground_group.add(ground)


# =======================================================================


# Game State
class GameState(pygame.sprite.Sprite, Sound, ):
    START_TIMER = pygame.time.get_ticks()

    def __init__(self, ):
        super().__init__()
        self.state = 'intro'
        self.current_music = Sound.intro_music(self)
        self.is_music_play = False
        self.background = None
        self.is_bg_created = False
        self.is_mushroom_created = False
        self.area = 2
        self.level = 1
        self.level_reader_row = 1

    def start_game(self):
        # top display frames
        table.update()
        # background_image('../src/assets/images/top_frames/4.png', 0, -5, False)

        # developer utils
        # text_creator(f'Direction: x= {int(player.direction.x)} y= {int(player.direction.y)}', 'white', 90, 15, 22)
        # text_creator(f'Pos: x= {int(player.pos.x)} y= {int(player.pos.y)}', 'white', 86, 33, 22)
        # text_creator(f'Vel: x= {player.velocity.x:.2f} y= {player.velocity.y:.2f} ', 'white', 90, 50, 22)
        # text_creator(f'Acc: x= {player.acceleration.x:.2f} y= {player.acceleration.y:.2f}', 'white', 90, 70, 22)

        # function sprite creator
        def sprite_creator(dictionary, input_class=None, group_class=None):
            time_now = pygame.time.get_ticks()
            # ---------create
            for k, v in dictionary.items():  # t: 'item pic'
                if k == int(self.background.distance_mt):
                    if time_now - self.START_TIMER > 300:  # timer prevent create double item in group
                        self.START_TIMER = time_now
                        if v in enemy_classes_dict:  # check is class
                            group_class.add(enemy_classes_dict[v])
                        else:
                            new_class = input_class(f'../src/assets/images/{v}.png')
                            group_class.add(new_class)
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
                case 1100:  # Finished level
                    Sound.sign_finish(self)
                    self.level += 1  # increase level
                    self.level_reader_row += 1  # read row level from txt
                    self.background.distance_mt = 0  # prevent ...
                    self.is_music_play = False
                    Sound.stop_all_sounds()
                    Sound.statistic_music(self)
                    self.state = 'level_statistic'  # switch to statistic state

        def area_label():  # Info Table label when Start new Area/Level
            if self.background.distance_mt < 10:
                image = pygame.image.load('../src/assets/images/frames/level_frame.png')
                SCREEN.blit(image, [SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 32])
                text_creator(f'Area {self.area} - {self.level}', 'white', SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2, 36)

        def current_areas_watcher():
            path = '../src/levels/current_area_levels.txt'
            file_operation(path, 'w', 0, f'{{"area": {self.area} , "level": {self.level}}}')

        # ============== level manipulator
        if self.level > 4:
            self.level = 1
            self.area += 1

        # save actual Area/Level on dict to txt file
        current_areas_watcher()

        # ========================================== START GAME  with Area 1; Level 1
        if self.area == 1:
            if not self.is_music_play:
                # self.current_music = Sound.forest_music_level_one(self)
                self.is_music_play = True

            if not self.is_bg_created:
                # resize image
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_1.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                self.is_bg_created = True

            # ============== create level: items, enemy, and more
            items_dict = eval(file_operation('levels/levels_data.txt', 'r', self.level_reader_row))
            sprite_creator(items_dict, Item, item_group)

            # ============= level counter
            distance_counter(item_group)

            # =================================================== UPDATE
            # update BG
            self.background.update()
            # --------------------------- draw sprite group
            # ground_group.draw(SCREEN)  # hide under bg
            bullets_group.draw(SCREEN)
            item_group.draw(SCREEN)
            player_group.draw(SCREEN)

            # --------------------------- update sprite group
            ground_group.update()
            item_group.update()
            bullets_group.update()
            player_group.update()

            # ============== draw current area/level labels
            area_label()

        if self.area == 2:
            print('AREA 2 ; Level 1')

    def intro(self):
        Intro()
        Intro.event(self)

    def menu(self):
        Menu()
        Menu().event(self)

    def legend(self):
        Legend()
        Legend().event(self)

    def score(self):
        Score()
        Score().event(self)

    def level_statistic(self):
        if screen_transition_animation() >= 0:  # clear screen
            LevelStatistic().event(self)
            LevelStatistic().update()

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


#  ================================ create new GameState
game_state = GameState()
# ================================================================ create top Table for: score , energy and more
table = Table(Bullet, all_spite_groups_dict)

# ============= Starting Game loop
while True:
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(FPS)
    exit_game()

