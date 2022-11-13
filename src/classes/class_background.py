import pygame
from src.settings import SCREEN, TOP_FRAME_SIZE, SCREEN_WIDTH, key_pressed, vec, text_creator, CLOCK


class Background:
    WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH // 3
    WALK_LEFT_SCREEN_BORDER = 80
    BG_SPEED = 3.33
    BG_SPEED_INCREASE = 2.67
    distance_mt = 0
    bg_counter = 0
    is_allowed_move = True

    def __init__(self, image=None, x=0, y=0, is_loop=False, speed=1, is_image_scaled=False,):
        self.image = image
        self.x = x
        self.y = y
        self.is_loop = is_loop
        self.speed = speed
        self.is_image_scaled = is_image_scaled

    def create_bg(self):
        if not self.is_image_scaled:
            bg_image = pygame.image.load(self.image).convert()  # convert make image fast
        else:
            bg_image = self.image.convert()
        if not self.is_loop:
            block_rect = bg_image.get_rect()
            SCREEN.blit(bg_image, (block_rect.x + self.x, block_rect.y + self.y))
        else:
            # draw bg screen loop animation
            rel_x = self.bg_counter % SCREEN_WIDTH
            SCREEN.blit(bg_image, (rel_x - SCREEN_WIDTH + 2,  self.y))
            if rel_x < SCREEN_WIDTH:
                SCREEN.blit(bg_image, (rel_x,  self.y))

            # ===============================================================   moving screen illusion
            if self.is_allowed_move:
                if key_pressed(pygame.K_RIGHT):
                    self.speed = self.BG_SPEED
                    self.speed = 3.33
                elif key_pressed(pygame.K_LEFT) and not self.WALK_LEFT_SCREEN_BORDER:
                    self.speed.x = -self.BG_SPEED
                    self.speed = 3.33
                else:
                    self.speed = 0

                # running screen illusion
                if key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_a):
                    self.speed += self.BG_SPEED_INCREASE

                self.bg_counter -= self.speed
                self.distance_mt += self.speed / 10

    def draw_label(self):
        pass
        # text_creator(f'BG_distance: {int(self.distance_mt)}', 'white', 290, 5)
        # text_creator(f'BG_speed: {self.speed:.2f}', 'white', 290, 20)

    def update(self):
        self.create_bg()
        self.draw_label()




