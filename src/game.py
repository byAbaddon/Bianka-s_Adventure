import pygame

from settings import *
from src.classes.class_sound import Sound
from state_classes import Intro, Menu, Legend, Score
from classes.class_player import Player
from classes.class_ground import Ground
from classes.class_bullet import Bullet
from classes.class_mushroom import Mushroom
from classes.class_background import Background


# ================================================================= TEST imported classes
# print(dir(Menu))

# ========================================================================== variables
level = 1

# ======================================================================== create Sprite groups
background_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
ground_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
mushroom_group = pygame.sprite.Group()

# add to all_sprite_groups
all_spite_groups_dict = {'player': player_group, 'ground': ground_group, 'bullets': bullets_group,
                         'mushroom': mushroom_group}
# ======================================================================= initialize  Classes

player = Player(Bullet, all_spite_groups_dict)
# for test before create classes group
# bullet = Bullet(x, y, player.direction)

ground = Ground()

# ground2 = Ground('../src/assets/images/ground/2.png', 100, SCREEN_HEIGHT - 150)
# ground3 = Ground('../src/assets/images/ground/2.png', 400, SCREEN_HEIGHT - 170)
mushroom = Mushroom()

# add to group
player_group.add(player)

ground_group.add(ground)
# for test before create classes group
# bullets_group.add(bullet)
mushroom_group.add(mushroom)

# =======================================================================


# Game State
class GameState(Sound, Background):
    def __init__(self):
        super().__init__()
        self.state = 'intro'
        self.current_music = Sound.intro_music(self)
        self.is_music_play = False
        self.background = None
        self.is_bg_created = False

    def start_game(self,):
        # developer utils

        text_creator(26, f'Direction: x= {int(player.direction.x)} y= {int(player.direction.y)}', 'white', 90, 10)
        text_creator(26, f'Pos: x= {int(player.pos.x)} y= {int(player.pos.y)}', 'white', 80, 30)
        text_creator(26, f'Vel: x= {player.velocity.x:.2f} y= {player.velocity.y:.2f} ', 'white', 90, 50)
        text_creator(26, f'Acc: x= {player.acceleration.x:.2f} y= {player.acceleration.y:.2f}', 'white', 90, 70)

        if level == 1:
            if not self.is_music_play:
                # self.current_music = Sound.forest_music_level_one(self)
                self.is_music_play = True
            if not self.is_bg_created:
                # resize image
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_1.png', 800, 510)

                # draw bg loop animation /send data: pic,x,y,loop, speed,start border, scaled
                # background_image(scaled_img, 0, 90, True, player.velocity.x, True)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                self.is_bg_created = True

            # update BG
            self.background.update()

            # draw sprite group
            # ground_group.draw(SCREEN)  # hide under bg
            player_group.draw(SCREEN)
            bullets_group.draw(SCREEN)
            mushroom_group.draw(SCREEN)

            # update sprite group
            ground_group.update()
            player_group.update()
            bullets_group.update()
            mushroom_group.update()

    def intro(self):
        Intro()
        Intro.event(self)

    def menu(self):
        Menu()
        Menu().event(self)

    def legend(self):
        Legend()
        Legend().event(self)

    def score(self):
        Score()
        Score().event(self)

    def state_manager(self):
        # print(self.state)
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

    # check and prevent fload, all sprite groups
    @staticmethod
    def sprite_cleaner():
        for k, v in all_spite_groups_dict.items():
            if len(v) >= 20:
                all_spite_groups_dict[k].empty()


#  ========================================================================== create new GameState
game_state = GameState()

# Starting Game
while True:
    exit_game()
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    game_state.sprite_cleaner()
    pygame.display.update()
    CLOCK.tick(FPS)
