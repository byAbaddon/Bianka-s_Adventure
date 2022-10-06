import pygame
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)


class Sound:
    @staticmethod
    def play_sound(sound_file, volume=0.5, loops=0):
        play = pygame.mixer.Sound(sound_file)
        play.set_volume(volume)
        play.play(loops)

    @staticmethod
    def stop_all_sounds():
        pygame.mixer.stop()

    def btn_click(self):
        self.play_sound('../src/assets/sounds/buttons/click.wav')

    def intro_music(self):
        self.play_sound('../src/assets/sounds/game_musics/intro_1.mp3')

    def game_over_music(self):
        self.play_sound('..src/assets/sounds/game_musics/game_over.mp3', 0.2, -1)

    # forest
    def forest_music_area_one(self):
        self.play_sound('../src/assets/sounds/game_musics/forest_1.mp3', 0.6, -1)

    # boss
    def boss_music_area_one(self):
        self.play_sound('../src/assets/sounds/game_musics/boss/boss_2.mp3', 0.6, -1)

    def statistic_music(self):
        self.play_sound('../src/assets/sounds/game_musics/statistic.mp3', 0.6, -1)

    def add_point(self):
        self.play_sound('../src/assets/sounds/point/point.wav')

    def player_jump(self):
        self.play_sound('../src/assets/sounds/player/jump.wav')

    def player_stone_hit(self):
        self.play_sound('../src/assets/sounds/player/stone_hit.wav')

    def player_enemy_hit(self):
        self.play_sound('../src/assets/sounds/player/enemy_hit.wav', 1)

    def player_shoot(self):
        self.play_sound('../src/assets/sounds/player/jump_shoot.wav', 1)

    def player_dead(self):
        self.play_sound('../src/assets/sounds/player/dead.wav', 1)

    def player_dead_funeral_march(self):
        self.play_sound('../src/assets/sounds/player/funeral_march.wav', 0.5, -1)

    def sign_go(self):
        self.play_sound('../src/assets/sounds/sign/go.wav', 1)

    def sign_middle(self):
        self.play_sound('../src/assets/sounds/sign/middle.wav')

    def sign_finish(self):
        self.play_sound('../src/assets/sounds/sign/finish.wav')

    def grab_mushroom(self):
        self.play_sound('../src/assets/sounds/player/grab.wav')

    def grab_poison_mushroom(self):
        self.play_sound('../src/assets/sounds/player/fart.mp3')

    def grab_coin(self):
        self.play_sound('../src/assets/sounds/player/grab_coin.wav')

    def grab_statuette(self):
        self.play_sound('../src/assets/sounds/player/grab_statuette.wav', 1)

    def grab_amulets(self):
        self.play_sound('../src/assets/sounds/player/grab_amulets.wav', 1)

    # enemy sound
    def mouse_sound(self):
        self.play_sound('../src/assets/sounds/enemies/mouse.wav', 1,)

    def mole_sound(self):
        self.play_sound('../src/assets/sounds/enemies/mole.wav', 1, )

    def monkey_sound(self):
        self.play_sound('../src/assets/sounds/enemies/monkey.wav', 1)

    def raven_sound(self):
        self.play_sound('../src/assets/sounds/enemies/raven.wav', 1)

    def boar_sound(self):
        self.play_sound('../src/assets/sounds/enemies/boar/boar.mp3', 1)

    def bee_sound(self):
        self.play_sound('../src/assets/sounds/enemies/bee/bee.wav', 1, 2)

    # player bullets hit something and kill enemy
    def bullet_ricochet(self):
        self.play_sound('../src/assets/sounds/bullet/ricochet.wav')

    def bullet_hit(self):
        self.play_sound('../src/assets/sounds/bullet/hit_item.wav')

    def bullet_statuette_hit(self):
        self.play_sound('../src/assets/sounds/bullet/hit_statuette.wav', 1)

    def bullet_fail(self):
        self.play_sound('../src/assets/sounds/bullet/fail.wav')

    def bullet_kill_boar(self):
        self.play_sound('../src/assets/sounds/enemies/boar/boar_squealing.wav')

    def bullet_kill_enemy(self):
        self.play_sound('../src/assets/sounds/enemies/bee/player_hit_bee.wav')

    # enemy bullets hit player
    def enemy_bullet_hit_player_head(self):
        self.play_sound('../src/assets/sounds/player/enemy_shooting_hit_head.wav', 0.5)

    def enemy_bullet_hit_player_body(self):
        self.play_sound('../src/assets/sounds/player/enemy_shooting_hit_body.wav', 1)

    # ==================================== BOSS KNIGHT
    def player_scream_die(self):
        self.play_sound('../src/assets/sounds/boss_knight/player_scream_die.wav', 1)

    def knight_scream(self):
        self.play_sound('../src/assets/sounds/boss_knight/knight_scream_time_to_kill.wav', 1)

    def bullet_player_hit_knight_face(self):
        self.play_sound('../src/assets/sounds/boss_knight/hit_face.wav', 1)

    def bullet_player_hit_knight_armor(self):
        self.play_sound('../src/assets/sounds/boss_knight/hit_armor.wav', 1)

    def knight_sword_slash(self):
        self.play_sound('../src/assets/sounds/boss_knight/sword_slash.wav', 1)

    def knight_jump(self):
        self.play_sound('../src/assets/sounds/boss_knight/jump.wav', 1)

    def knight_walk(self):
        self.play_sound('../src/assets/sounds/boss_knight/walk.wav', 1)

    def knight_dead(self):
        self.play_sound('../src/assets/sounds/boss_knight/dead.wav', 1)
