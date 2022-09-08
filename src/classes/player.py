import pygame
# from src.game import SCREEN_WIDTH, SCREEN_HEIGHT


class Player(pygame.sprite.Sprite):
    energy_power = 100
    player_dead = False
    counter = 0

    # def __init__(self, pos=(SCREEN_WIDTH - 700, SCREEN_HEIGHT - 80)):
    def __init__(self, x=100, y=470):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../src/assets/images/player/right_profile/11.png')
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (x, y)
    #   self.position = SCREEN_WIDTH - 700  # player start position
        self.direction = 1  # go right ; -1 go left
        self.speed = 0  # player speed

    def flip_image(self):
        if self.direction == -1:
            self.image = pygame.transform.flip(pygame.image.load(self.image), True, False)

    def update(self):
        pygame.mask.from_surface(self.image)  # create mask image
