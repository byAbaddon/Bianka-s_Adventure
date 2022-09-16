import pygame

from settings import *
from src.classes.class_sound import Sound
from state_classes import Intro, Menu, Legend, Score
from classes.class_player import Player
from classes.class_ground import Ground
from classes.class_bullet import Bullet


# ================================================================= TEST imported classes
# print(dir(Menu))

# ========================================================================== variables
level = 1

# ======================================================================== create Sprite groups
player_group = pygame.sprite.GroupSingle()
ground_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

# add to all_sprite_groups
all_spite_groups_dict = {'player': player_group, 'ground': ground_group, 'bullets': bullets_group}
# ======================================================================= initialize  Classes

player = Player(Bullet, all_spite_groups_dict)
# for test before create classes group
# bullet = Bullet(player.shot_position, player.direction)
ground = Ground()
# ground2 = Ground('../src/assets/images/ground/2.png', 100, SCREEN_HEIGHT - 150)
# ground3 = Ground('../src/assets/images/ground/2.png', 400, SCREEN_HEIGHT - 170)


# add to group
player_group.add(player)
ground_group.add(ground)
# for test before create classes group
# bullets_group.add(bullet)


# =======================================================================
# Game State
class GameState(Sound):
    def __init__(self):
        super().__init__()
        self.state = 'intro'
        self.current_music = Sound.intro_music(self)
        self.is_music_play = False

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

            # draw bg loop animation
            background_image('../src/assets/images/backgrounds/bg_forest_2.png', 0, 102., True)

            # draw sprite group
            ground_group.draw(SCREEN)
            player_group.draw(SCREEN)
            bullets_group.draw(SCREEN)

            # update sprite group
            ground_group.update()
            player_group.update()
            bullets_group.update()

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


#  ========================================================================== create new GameState
game_state = GameState()

# Starting Game
while True:
    exit_game()
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(FPS)

