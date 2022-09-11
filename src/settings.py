import pygame

# display size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# add icon
programIcon = pygame.image.load('assets/images/title_icon/girl.png')
pygame.display.set_icon(programIcon)

# add caption
pygame.display.set_caption('*** Bianka\'s Adventure ***', 'default_icon')

# ========================================================================== global const
# clock frames
CLOCK = pygame.time.Clock()

