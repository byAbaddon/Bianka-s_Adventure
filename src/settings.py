import pygame
from sys import exit
from pygame.math import Vector2

vec = Vector2
# ========================================================================== initialize
pygame.init()
# pygame.mixer.init()

# hide mouse from game window
# pygame.mouse.set_visible(False)
# ========================================================================== display size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# ========================================================================== add icon
programIcon = pygame.image.load('assets/images/title_icon/girl.png')
pygame.display.set_icon(programIcon)

# ========================================================================== add caption
pygame.display.set_caption('*** Bianka\'s Adventure ***', 'default_icon')

# ========================================================================== global const
# clock frames
CLOCK = pygame.time.Clock()
FPS = 60

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
