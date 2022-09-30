import pygame

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
    PICTURE_DICT = {'statuette': 'bonus/statuette_big'}

    def __init__(self,):
        super().__init__()
        self.state = ''

    def info_statistic(self):
        text_creator(f'MousePos: x= {pygame.mouse.get_pos()}', 'white', 490, 15)
        # add music
        text_creator("CONGRATULATIONS", 'red', SCREEN_WIDTH // 2, 130, 55, None, None, True)

        text_creator("Idol: 1000 pst", 'yellow', 270, 400, 36)
        image = pygame.image.load(f'../src/assets/images/{self.PICTURE_DICT["statuette"]}.png')
        SCREEN.blit(image, [440, 340])

    def play_music(self):
        pass

    def update(self):
        self.info_statistic()

    @staticmethod
    def event(self):
        if key_pressed(pygame.K_SPACE):
            self.state = 'start_game'
            Sound.btn_click(self)
            Sound.stop_all_sounds()
