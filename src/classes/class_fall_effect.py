import pygame
from src.settings import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH, TOP_FRAME_SIZE, GROUND_HEIGHT_SIZE,\
    randrange, key_pressed
from src.classes.class_sound import Sound


class FallEffect(pygame.sprite.Sprite, Sound):
    snow_list = []
    start_time = pygame.time.get_ticks()
    COOLDOWN = 1000

    def __init__(self, fall_type='snow | rein | confetti', color='white', size=2, speed=4, static=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../src/assets/images/fail_items/empty_pixel_image.png')
        self.rect = self.image.get_rect()
        self.size = size
        self.color = color
        self.speed = speed
        self.fail_type = fall_type
        self.static = static

    def fail_effect_creator(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.start_time > self.COOLDOWN:
            self.start_time = time_now
            x = randrange(0, SCREEN_WIDTH)
            y = randrange(TOP_FRAME_SIZE, SCREEN_HEIGHT)
            self.snow_list.append([x, y])

    def snow_creator(self):
        for i in self.snow_list:
            i[1] += self.speed  # add speed gravity
            if i[1] > SCREEN_HEIGHT:  # - GROUND_HEIGHT_SIZE   =   border fall
                i[0] = randrange(SCREEN_WIDTH)
                i[1] = randrange(95, TOP_FRAME_SIZE)
            if key_pressed(pygame.K_RIGHT) and not self.static:
                i[0] -= 2.3
            pygame.draw.circle(SCREEN, self.color, i, self.size)

    def rein_creator(self):
        for i in self.snow_list:
            i[1] += self.speed  # add speed gravity
            i[0] -= 1  # add speed gravity
            if i[1] > SCREEN_HEIGHT: # - GROUND_HEIGHT_SIZE   =   border fall
                i[0] = randrange(SCREEN_WIDTH)
                i[1] = randrange(95, TOP_FRAME_SIZE)
            if key_pressed(pygame.K_RIGHT):
                i[0] -= 2
            pygame.draw.line(SCREEN, self.color, i, (i[0] - 1, i[1]), 4)

    def confetti_creator(self):
        for i in self.snow_list:
            i[1] += self.speed  # add speed gravity
            if i[1] > SCREEN_HEIGHT - GROUND_HEIGHT_SIZE:
                i[0] = randrange(SCREEN_WIDTH)
                i[1] = randrange(95, TOP_FRAME_SIZE)
            pygame.draw.line(SCREEN, (randrange(0, 255), randrange(0, 255), randrange(0, 255)), i,
                             (i[0] - 1, i[1] + 15), randrange(1, 10))
            # pygame.draw.circle(SCREEN, (randrange(0, 255), randrange(0, 255), randrange(0, 255)), i, randrange(5, 10))

    def make_sound(self):
        pass

    def update(self):
        self.fail_effect_creator()
        self.make_sound()
        if self.fail_type == 'snow':
            self.snow_creator()
        elif self.fail_type == 'rein':
            self.rein_creator()
        elif self.fail_type == 'confetti':
            self.confetti_creator()
