import pygame
from sys import exit


pygame.init()

# display size
WIDTH, HEIGHT = 800, 600
pygame.display.set_mode((WIDTH, HEIGHT))

# add icon
programIcon = pygame.image.load('assets/images/title_icon/girl.png')
pygame.display.set_icon(programIcon)

# add caption
pygame.display.set_caption('*** Bianka\'s Adventure ***', 'default_icon')


# clock frames
clock = pygame.time.Clock()


# Starting Game

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



