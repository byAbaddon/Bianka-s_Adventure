import pygame
from sys import exit
from settings import *
from classes import class_sound, class_ground, class_player, class_bullet

pygame.init()

# ========================================================================== variables
level = 1

# print(dir(class_player))

# ========================================================================= global methods


# draw background
def background_image(image, x=0, y=0):
    bg_image = pygame.image.load(image).convert()
    block_rect = bg_image.get_rect()
    SCREEN.blit(bg_image, (block_rect.x + x, block_rect.y + y))


# create text
def text_creator(font_size=26, text='No Text', rgb_color=(255, 255, 255),
                 x_pos=SCREEN_WIDTH // 2, y_pos=SCREEN_HEIGHT // 2):
    font = pygame.font.Font(None, font_size)
    input_text = font.render(text, True, rgb_color)
    text_position = input_text.get_rect(center=(x_pos, y_pos))
    SCREEN.blit(input_text, text_position)


# keyboard events for exit
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# ======================================================================= initialize  Classes
play_sound = class_sound.Sound()
player = class_player.Player()
ground = class_ground.Ground()
ground2 = class_ground.Ground('../src/assets/images/ground/2.png', 200, SCREEN_HEIGHT - 280)
bullet = class_bullet.Bullet(player.shooting_bullet_position())

# ======================================================================== create Sprite groups
player_group = pygame.sprite.GroupSingle()
ground_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

# add to group
player_group.add(player)
ground_group.add(ground, ground2)
bullets_group.add(bullet)


# =======================================================================
# Game State
class GameState:
    def __init__(self):
        self.state = 'intro'
        self.current_music = play_sound.intro_music()
        self.is_music_play = False

    def intro(self):
        background_image('../src/assets/images/backgrounds/bg_intro.png')
        text_creator(26, 'Copyright - 2022', (211, 0, 0), 80, SCREEN_HEIGHT - 20)
        text_creator(26, 'By Abaddon', (211, 0, 0), SCREEN_WIDTH - 60, SCREEN_HEIGHT - 20)
        text_creator(36, 'Start Game: SpaceBar', (255, 255, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        text_creator(36, 'MENU: Return', (255, 255, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.state = 'menu'
            play_sound.btn_click()
        if keys[pygame.K_SPACE]:
            self.state = 'start_game'
            play_sound.stop_all_sounds()  # if eny music play stop it

    def menu(self):
        background_image('../src/assets/images/backgrounds/bg_controls.png')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.state = 'intro'
            play_sound.btn_click()
        if keys[pygame.K_LEFT]:
            self.state = 'legend'
            play_sound.btn_click()
        if keys[pygame.K_RIGHT]:
            self.state = 'score'
            play_sound.btn_click()

    def legend(self):
        background_image('../src/assets/images/backgrounds/bg_legend.png')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.state = 'intro'
            play_sound.btn_click()

    def score(self):
        background_image('../src/assets/images/backgrounds/bg_legend.png')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.state = 'intro'
            play_sound.btn_click()

    def start_game(self):
        # ground and player collide
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if hits:
            player.rect.y = hits[0].rect.top - player.PLAYER_HEIGHT_SIZE
            player.gravity = 0
        else:
            player.gravity = 5

        if level == 1:
            if not self.is_music_play:
                self.current_music = play_sound.forest_music_level_one()
                self.is_music_play = True
            background_image('../src/assets/images/backgrounds/bg_forest.jpg', 0, 100)

            # draw sprite group
            ground_group.draw(SCREEN)
            player_group.draw(SCREEN)
            bullets_group.draw(SCREEN)

            # update sprite group
            ground_group.update()
            player_group.update()
            bullets_group.update()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'menu':
            self.menu()
        if self.state == 'legend':
            self.legend()
        if self.state == 'score':
            self.score()
        if self.state == 'start_game':
            self.start_game()


#  ========================================================================== create new GameState
game_state = GameState()

# Starting Game
while True:
    exit_game()
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(60)
