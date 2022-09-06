import pygame
from sys import exit

pygame.init()

# display size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# add icon
programIcon = pygame.image.load('assets/images/title_icon/girl.png')
pygame.display.set_icon(programIcon)

# add caption
pygame.display.set_caption('*** Bianka\'s Adventure ***', 'default_icon')

# clock frames
clock = pygame.time.Clock()


# ========================================================================= global methods

# draw background
def background_image(image):
    bg_image = pygame.image.load(image)
    block_rect = bg_image.get_rect()
    SCREEN.blit(bg_image, (block_rect.x, block_rect.y))


# create text
def text_creator(font_size=26, text='No Text', rgb_color=(255, 255, 255),
                 x_pos=SCREEN_WIDTH // 2, y_pos=SCREEN_HEIGHT // 2):
    font = pygame.font.Font(None, font_size)
    input_text = font.render(text, True, rgb_color)
    text_position = input_text.get_rect(center=(x_pos, y_pos))
    SCREEN.blit(input_text, text_position)



# =========================================================================

# Game State
class GameState:
    def __init__(self):
        self.state = 'intro'

    def intro(self):
        background_image('../src/assets/images/backgrounds/bg_game_over_1000_800.jpeg')
        text_creator(26, 'Copyright - 2022', (0, 160, 255), 80, SCREEN_HEIGHT - 20)
        text_creator(26, 'By Abaddon', (0, 160, 255), SCREEN_WIDTH - 60, SCREEN_HEIGHT - 20)

    def legend(self):
        background_image('../src/assets/images/backgrounds/bg_controls_img.png')

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'legend':
            self.legend()

#  ========================================================================== create new GameState
game_state = GameState()

# Starting Game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    clock.tick(60)
    time_counter = pygame.time.get_ticks()
