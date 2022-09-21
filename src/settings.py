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

# ==================================================================== local variables
GROUND_HEIGHT_SIZE = 78
BG_SPEED = 3.33
BG_LOOP_SPEED_INCREASE = 2.27
WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH // 3
bg_counter = 0
bg_current_speed = 0


# draw background :Player data:  speed=1, p_pos_x=100, start_border_run=0,
def background_image(image, x=0, y=0, loop=False, speed=1, p_direction_y=1, is_image_scaled=False):
    global bg_counter, bg_current_speed
    if not is_image_scaled:
        bg_image = pygame.image.load(image).convert()  # convert make image fast
    else:
        bg_image = image
    if not loop:
        block_rect = bg_image.get_rect()
        SCREEN.blit(bg_image, (block_rect.x + x, block_rect.y + y))
    else:
        # draw bg screen loop animation
        rel_x = bg_counter % SCREEN_WIDTH
        SCREEN.blit(bg_image, (rel_x - SCREEN_WIDTH + 2, y))
        if rel_x < SCREEN_WIDTH:
            SCREEN.blit(bg_image, (rel_x, y))

        # # set start_border and speed
        if key_pressed(pygame.K_RIGHT) and WALK_RIGHT_SCREEN_BORDER:
            speed = BG_SPEED
        # running illusion screen
        right_up_pressed = key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_UP)
        right_pressed_pos_y = key_pressed(pygame.K_RIGHT) and p_direction_y == -1

        # and key_pressed(pygame.K_a) and p_direction_y != -1:
        if key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_a) and not (right_up_pressed or right_pressed_pos_y):
            speed = BG_SPEED + BG_LOOP_SPEED_INCREASE
        if key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_a) and key_pressed(pygame.K_UP):
            speed = BG_SPEED + BG_LOOP_SPEED_INCREASE
        bg_counter -= speed
        bg_current_speed = speed


# create text
def text_creator(font_size=26, text='No Text', rgb_color=(255, 255, 255),
                 x_pos=SCREEN_WIDTH // 2, y_pos=SCREEN_HEIGHT // 2, background=None):
    font = pygame.font.Font(None, font_size)
    input_text = font.render(text, True, rgb_color, background)
    text_position = input_text.get_rect(center=(x_pos, y_pos))
    SCREEN.blit(input_text, text_position)


# resize image
def scale_image(image, x_size, y_size):
    scaled_image = pygame.transform.scale(pygame.image.load(image), (x_size, y_size))
    return scaled_image.convert()


# check key pressed or released
def key_pressed(input_key=None):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[input_key]:  # pygame.K_SPACE
        return True
    return False


# keyboard events for exit
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
