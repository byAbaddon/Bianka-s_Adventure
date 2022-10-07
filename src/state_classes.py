from src.settings import *
from src.classes.class_sound import Sound


# =========================================== Intro state class============================================
class Intro(Sound):
    def __init__(self):
        super().__init__()
        background_image('../src/assets/images/backgrounds/bg_intro.png')
        text_creator('Copyright - 2022', (211, 0, 0), 20, SCREEN_HEIGHT - 20,)
        text_creator('By Abaddon', (211, 0, 0), SCREEN_WIDTH - 130, SCREEN_HEIGHT - 20,)
        text_creator('Start Game: SpaceBar', (255, 255, 200), SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 36)
        text_creator('MENU: Return', (255, 255, 200), SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140, 36)
        self.state = ''

    def event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            Sound.btn_click(self)
            self.state = 'menu'
        if keys[pygame.K_SPACE]:
            Sound.stop_all_sounds()  # if eny music play stop it
            self.state = 'start_game'
            # self.state = 'boss'


# =========================================== Menu state class ============================================
class Menu(Sound):
    def __init__(self):
        super().__init__()
        background_image('../src/assets/images/backgrounds/bg_controls.png')
        self.state = ''

    @staticmethod
    def event(self):
        if key_pressed(pygame.K_UP):
            Sound.btn_click(self)
            self.state = 'intro'
        if key_pressed(pygame.K_LEFT):
            Sound.btn_click(self)
            self.state = 'legend'
        if key_pressed(pygame.K_RIGHT):
            Sound.btn_click(self)
            self.state = 'score'


# =========================================== Legend state class =============================================
class Legend(Sound):
    def __init__(self):
        super().__init__()
        background_image('../src/assets/images/backgrounds/bg_legend.png')
        self.state = ''

    @staticmethod
    def event(self):
        if key_pressed(pygame.K_RIGHT):
            Sound.btn_click(self)
            self.state = 'intro'


# =========================================== Score state class ============================================
class Score(Sound):
    def __init__(self):
        super().__init__()
        background_image('../src/assets/images/backgrounds/bg_legend.png')
        self.state = ''

    @staticmethod
    def event(self):
        if key_pressed(pygame.K_LEFT):
            Sound.btn_click(self)
            self.state = 'intro'


# =========================================== LevelStatistic class
class LevelStatistic(Sound):
    def __init__(self, bonus_pts, player_data, level):
        self.state = ''
        self.bonus_pts = bonus_pts
        self.player_data = player_data
        self.level = level

    def info_statistic(self):
        text_creator(f'MousePos: x= {pygame.mouse.get_pos()}', 'white', 490, 5)

        text_creator("CONGRATULATIONS", 'red', 200, 230, 55, None, None, True)

        if not self.player_data.is_player_kill_boss:
            # bonus point
            text_creator(f'Bonus Points', 'yellow', 336, 320, 30)
            text_creator(f'{self.bonus_pts}', 'yellow', 372, 350, 36)
            image = pygame.image.load(f'../src/assets/images/frames/down_left.png')
            SCREEN.blit(image, [300, 300])
            image = pygame.image.load(f'../src/assets/images/frames/down_right.png')
            SCREEN.blit(image, [400, 300])
            # coin
            image = pygame.image.load(f'../src/assets/images/bonus/coin_medium.png')
            SCREEN.blit(image, [150, 400])
            text_creator(f'x {self.player_data.bonus_coins} = {self.player_data.bonus_coins * 1000}', 'yellow', 220, 430, 30)
            # idol
            text_creator(f'{self.player_data.bonus_statuette * 3000} = {self.player_data.bonus_statuette} x', 'yellow', 480, 430, 30)
            image = pygame.image.load(f'../src/assets/images/bonus/statuette_medium.png')
            SCREEN.blit(image, [580, 360])
        else:
            # bonus point
            text_creator(f'Bonus Points', 'yellow', 336, 410, 30)
            text_creator(f'{self.bonus_pts}', 'yellow', 372, 440, 36)
            image = pygame.image.load(f'../src/assets/images/frames/down_left.png')
            SCREEN.blit(image, [300, 380])
            image = pygame.image.load(f'../src/assets/images/frames/down_right.png')
            SCREEN.blit(image, [400, 380])
            # amulet
            text_creator(f'1  x', 'yellow', 280, 320, 30)
            text_creator(f'{5000}', 'yellow', 480, 320, 30)
            amulet_img = f'../src/assets/images/amulets/big/{self.player_data.boss_taken_amulets}.png'
            scaled_amulet = scale_image(amulet_img, 100, 100)
            SCREEN.blit(scaled_amulet, [SCREEN_WIDTH // 2 - 50, 270])

    def update(self):
        self.info_statistic()

    @staticmethod
    def event(self):
        if key_pressed(pygame.K_SPACE) and self.player_data.energy_power == 0:
            self.player_data.reset_current_player_data()  # rest energy player and more...
            Sound.stop_all_sounds()
            self.state = 'start_game'
            if not self.player_data.is_player_kill_boss:
                self.level += 1  # increase level


# =========================================== GameOver class
class PlayerDead(Sound):
    def __init__(self, player_data, area, level):
        self.state = ''
        self.player_data = player_data
        self.area = area
        self.level = level

        background_image('../src/assets/images/player/cry/cry.png', 70, 70)
        text_creator('Ha-ha-ha', 'orange', SCREEN_WIDTH - 155, 15)
        text_creator('He will be mine...', 'orange', SCREEN_WIDTH - 155, 35)

        scaled_image = scale_image('../src/assets/images/wizard/wizard_two.png', 300, 200)
        SCREEN.blit(scaled_image, [480, 40])

        text_creator('You are dead!', 'red', 390, 340, 50)
        text_creator(f'Area: {self.area} / Level: {self.level}', 'yellow', 510, 380)
        text_creator(f'Lives: {self.player_data.lives}', 'green', 620, 410)

        text_creator('Press Space to try again...', 'white', SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT - 30)

    def event(self):
        if key_pressed(pygame.K_SPACE):
            Sound.stop_all_sounds()
            Sound.btn_click(self)
            self.state = 'start_game'






