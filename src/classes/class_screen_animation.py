import pygame
from src.settings import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from src.classes.class_player import Player
from src.classes.class_bullet import Bullet


class ScreenAnimation(Player):
    def __init__(self, pic='../src/assets/images/level_statistic/bg_statistic.png'):
        Player(Bullet).__init__(self)
        self.x = SCREEN_WIDTH
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.image = pygame.image.load(pic)
        self.rect = self.image.get_rect()

    def screen_animation(self):
        SCREEN.fill('black', [self.x, self.y, self.width, self.height])
        if self.x > 0:
            self.x -= 10
        else:
            self.stop_all_sounds()
            SCREEN.blit(self.image, (0, 0))

    def update(self):
        self.screen_animation()
