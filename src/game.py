from settings import *
from src.classes.class_sound import Sound
from state_classes import Intro, Menu, Legend, Score

from sprite_classes import Player, Ground, Bullet


# ================================================================= TEST imported classes
# print(dir(Menu))

# ========================================================================== variables
level = 1


# ======================================================================= initialize  Classes

player = Player()
ground = Ground()
ground2 = Ground('../src/assets/images/ground/2.png', 200, SCREEN_HEIGHT - 280)
bullet = Bullet(player.shooting_bullet_position())

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

    def start_game(self):
        # ground and player collide
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if hits:
            player.rect.y = hits[0].rect.top - player.PLAYER_HEIGHT_SIZE
            player.gravity = 0
            player.direction = 0

        else:
            player.gravity = 5
            player.is_ground = False

        if level == 1:
            if not self.is_music_play:
                self.current_music = Sound.forest_music_level_one(self)
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
    CLOCK.tick(60)
