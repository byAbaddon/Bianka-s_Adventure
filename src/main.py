# import pygame
# import random
# from sys import exit
# # from sprites import *
#
# # ========================================================================== initialize
# pygame.init()
# # pygame.mixer.init()
# # ========================================================================== display size
# SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
# SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# # ========================================================================== add icon
# programIcon = pygame.image.load('assets/images/title_icon/girl.png')
# pygame.display.set_icon(programIcon)
#
# # ========================================================================== add caption
# pygame.display.set_caption('*** Bianka\'s Adventure ***', 'default_icon')
#
# # ========================================================================== global const
# # clock frames
# CLOCK = pygame.time.Clock()
# FPS = 60
# # ========================================================================== variables
# level = 1
#
# # ================================================================= TEST imported classes
# # print(dir(class_player))
#
#
# class Game:
#     def __init__(self):
#         # initialize game window, etc
#         self.clock = CLOCK
#         self.running = True
#
#     def new(self):
#         # start a new game
#         # self.all_sprites = pygame.sprite.Group()
#         # self.player = Player()
#         # self.all_sprites.add(self.player)
#         self.run()
#
#     def run(self):
#         # Game Loop
#         self.playing = True
#         while self.playing:
#             self.clock.tick(FPS)
#             self.events()
#             self.update()
#             self.draw()
#
#     def update(self):
#         # Game Loop - Update
#         self.all_sprites.update()
#
#     def events(self):
#         # Game Loop - events
#         for event in pygame.event.get():
#             # check for closing window
#             if event.type == pygame.QUIT:
#                 if self.playing:
#                     pass
#                     # self.playing = False
#                 self.running = False
#
#     def draw(self):
#         # Game Loop - draw
#         self.screen.fill('black')
#         self.all_sprites.draw(self.screen)
#         # *after* drawing everything, flip the display
#         pygame.display.flip()
#
#     def show_start_screen(self):
#         # game splash/start screen
#         pass
#
#     def show_go_screen(self):
#         # game over/continue
#         pass
#
#
# g = Game()
# g.show_start_screen()
# while g.running:
#     g.new()
#     g.show_go_screen()
#
# pygame.quit()