import pygame

from src.settings import *
from src.classes.class_sound import Sound


# =========================================== Intro state class============================================
class Intro(Sound):
    def __init__(self):
        super().__init__()
        background_image('../src/assets/images/backgrounds/bg_intro.png')
        text_creator(26, 'Copyright - 2022', (211, 0, 0), 80, SCREEN_HEIGHT - 20)
        text_creator(26, 'By Abaddon', (211, 0, 0), SCREEN_WIDTH - 60, SCREEN_HEIGHT - 20)
        text_creator(36, 'Start Game: SpaceBar', (255, 255, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        text_creator(36, 'MENU: Return', (255, 255, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
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
    def __init__(self, pic='../src/assets/images/level_statistic/bg_statistic.png'):
        super().__init__()
        self.state = ''
        self.x = SCREEN_WIDTH
        self.y = 0
        self.image = pygame.image.load(pic)
        self.rect = self.image.get_rect()
        self.is_fill = False

        Sound.stop_all_sounds()
        if not self.is_fill:
            SCREEN.fill('red', [self.x - 200, self.y, SCREEN_WIDTH, SCREEN_HEIGHT])
            self.is_fill = True

    def screen_animation(self):

        if self.x > 0:
            self.x -= 10
        else:
            SCREEN.blit(self.image, (0, 0))

    def update(self):
        self.screen_animation()
        print(self.x)

    @staticmethod
    def event(self):
        if key_pressed(pygame.K_SPACE):
            self.state = 'intro'
            Sound.btn_click(self)
