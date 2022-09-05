import pygame

pygame.init()

# display size
WIDTH, HEIGHT = 800, 600
pygame.display.set_mode((WIDTH, HEIGHT))

# add caption
pygame.display.set_caption('*** Bianka\'s Adventure ***')

# add icon
# programIcon = pygame.image.load('../icons/snakes.png')
# pygame.display.set_icon(programIcon)

# clock frames
clock = pygame.time.Clock()


# Starting Game
run_game = True
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False


pygame.quit()


