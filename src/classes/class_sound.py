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
        self.play_sound('../src/assets/sounds/game_musics/intro.mp3')

    # =================================== areas bg music

    # Area 1 forest
    def forest_music_area_one(self):
        self.play_sound('../src/assets/sounds/game_musics/level_1.mp3', 0.6, -1)

    # Area 2 See
    def sea_music_area_two(self):
        self.play_sound('../src/assets/sounds/game_musics/level_2.mp3', 0.6, -1)

    # Area 3 Volcano
    def volcano_music_area_three(self):
        self.play_sound('../src/assets/sounds/game_musics/level_3.mp3', 0.6, -1)

    # Level 3 Ice Age
    def ice_music_area_four(self):
        self.play_sound('../src/assets/sounds/game_musics/level_4.mp3', 0.5, -1)

    # Level 5 Dark Forest
    def dark_forest_music_area_five(self):
        self.play_sound('../src/assets/sounds/game_musics/level_5.mp3', 0.5, -1)

    # Level 6 Sea Two
    def sea_two_music_area_six(self):
        self.play_sound('../src/assets/sounds/game_musics/level_6.mp3', 0.5, -1)

    # Level 7 Desert
    def desert_music_area_seven(self):
        self.play_sound('../src/assets/sounds/game_musics/level_7.mp3', 0.5, -1)

    # Level 9 Castle
    def castle_music_area_nine(self):
        self.play_sound('../src/assets/sounds/game_musics/level_9.mp3', 0.4, -1)

    # ======================================   BOSS
    def boss_music_area_one(self):
        self.play_sound('../src/assets/sounds/game_musics/boss/boss_2.mp3', 0.5, -1)

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
        self.play_sound('../src/assets/sounds/player/dead.wav', 0.5)

    def player_injury(self):
        self.play_sound('../src/assets/sounds/player/injury_trap.mp3', 1)

    def player_fail_in_water(self):
        self.play_sound('../src/assets/sounds/splashes/splashes.wav', 1)

    def sign_go(self):
        self.play_sound('../src/assets/sounds/sign/go.wav', 1)

    def sign_middle(self):
        self.play_sound('../src/assets/sounds/sign/middle.wav')

    def sign_finish(self):
        self.play_sound('../src/assets/sounds/sign/finish.wav')

    def grab_item(self):
        self.play_sound('../src/assets/sounds/player/grab.wav')

    def grab_poison_mushroom(self):
        self.play_sound('../src/assets/sounds/player/fart.mp3')

    def grab_coin(self):
        self.play_sound('../src/assets/sounds/player/grab_coin.wav', 1)

    def grab_statuette(self):
        self.play_sound('../src/assets/sounds/player/grab_statuette.wav', 1)

    def grab_amulets(self):
        self.play_sound('../src/assets/sounds/player/grab_amulets.wav', 1)

    def snapping_trap(self):
        self.play_sound('../src/assets/sounds/trap/snapping_trap.wav', 1)

    # -------------------------------------------   enemy sound
    def snowmen_sound(self):
        self.play_sound('../src/assets/sounds/enemies/snowmen.wav', 1,)

    def mouse_sound(self):
        self.play_sound('../src/assets/sounds/enemies/mouse.wav', 1,)

    def penguin_sound(self):
        self.play_sound('../src/assets/sounds/enemies/penguin.wav', 1,)

    def seal_sound(self):
        self.play_sound('../src/assets/sounds/enemies/seal.wav', 1, )

    def ghost_sound(self):
        self.play_sound('../src/assets/sounds/enemies/ghost.wav', 0.3, 2)

    def cockroach_sound(self):
        self.play_sound('../src/assets/sounds/enemies/cockroach.wav', 0.3,)

    def octopus_sound(self):
        self.play_sound('../src/assets/sounds/enemies/octopus.mp3', 1, )

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

    def crab_sound(self):
        self.play_sound('../src/assets/sounds/enemies/crab/crab.wav', 0.2, 2)

    def fish_sound(self):
        self.play_sound('../src/assets/sounds/enemies/fish.wav', 0.5,)

    def vulture_sound(self):
        self.play_sound('../src/assets/sounds/enemies/vulture.wav', 0.5, 1)

    def dragon_sound(self):
        self.play_sound('../src/assets/sounds/enemies/dragon.mp3', 0.3, 1)

    def turtle_sound(self):
        self.play_sound('../src/assets/sounds/enemies/turtle.wav', 1, 2)

    def monster_sound(self):
        self.play_sound('../src/assets/sounds/enemies/monster.wav', 1, 2)

    def thunder_sound(self):
        self.play_sound('../src/assets/sounds/enemies/volcano/thunder.wav', 0.1)

    def fireball_sound(self):
        self.play_sound('../src/assets/sounds/enemies/volcano/fireball.wav', 1)

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
        self.play_sound('../src/assets/sounds/boss_knight/player_scream_die.wav', 0.5)

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

    # ============================================ dead and game over
    # lost_live
    def player_dead_funeral_march(self):
        self.play_sound('../src/assets/sounds/player/funeral_march.wav', 0.5, -1)

    def player_lost_live_music(self):
        self.play_sound('../src/assets/sounds/dead_live/dead_live.mp3', 0.2, -1)

    def fail_in_sea(self):
        self.play_sound('../src/assets/sounds/splashes/splashes.wav', 1)

    def game_over_voice(self):
        self.play_sound('../src/assets/sounds/game_over/game-over_voice.wav', 1,)
