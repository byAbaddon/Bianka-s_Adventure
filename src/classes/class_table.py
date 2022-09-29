from src.settings import *
from src.classes.class_player import Player


class Table(Player):
    height_score = 3000
    boss_energy = 200

    def __init__(self, class_bullet, all_sprite_groups_dict):
        Player.__init__(self, class_bullet, all_sprite_groups_dict)
        self.area = 0
        self.level = 0
        self.score = Player.score
        self.energy_power = Player.energy_power
        self.lives = Player.lives

    def get_current_area_level(self):
        try:
            data_dict = eval(file_operation('../src/levels/current_area_levels.txt', 'r'))
            self.area = data_dict['area']
            self.level = data_dict['level']
        except:
            print('Unable load level from txt file')

    @staticmethod
    def create_top_frame():
        background_image('../src/assets/images/top_frames/4.png', 0, -5, False)

    def get_top_score_from_file(self):
        self.height_score = file_operation('src/score/save_height_score.txt', 'r', 0)

    def write_new_height_score_in_file(self):  # write new score record in file
        if self.score >= self.height_score:
            file_operation('../src/score/save_height_score.txt', 'w', 0, self.height_score)

    def draw_top_score(self):
        if self.score >= self.height_score:
            self.height_score = self.score
        text_creator(f'TopScore: {self.height_score}', (255, 200, 0), 21, 25, 30)

    def draw_current_score(self):
        t = text_creator(f'Score: {self.score}', 'white', 57, 46, 29)

    def draw_lives(self):
        text_creator(f'Lives: {self.lives}', 'white', 58, 68, 29)
        image = pygame.image.load('../src/assets/images/title_icon/baby_hat.png').convert()
        SCREEN.blit(image, (20, 42))

    def draw_area_and_level(self):
        text_creator(f'Area:  {self.area}', (255, 200, 0), SCREEN_WIDTH - 92, 24, 29)
        text_creator(f'Level: {self.level}', (255, 200, 0), SCREEN_WIDTH - 92, 44, 29)

    def energy_bar(self):
        text_creator('Bianka', 'white', 328, 67, 29)

        bar = pygame.Rect(400, 60, 100, 16)
        pygame.draw.rect(SCREEN, 'red', bar, border_radius=2)
        # up green
        bar = pygame.Rect(400, 60, self.energy_power, 16)
        pygame.draw.rect(SCREEN, (0, 200, 0), bar, border_radius=2)

    def energy_bar_boss(self):
        text_creator('Boss', 'white', 527, 67, 29)
        # bottom red
        bar = pygame.Rect(SCREEN_WIDTH - 219, 60, 200, 16)
        pygame.draw.rect(SCREEN, 'red', bar, border_radius=2)
        # up blue
        bar = pygame.Rect(SCREEN_WIDTH - 219, 60, self.boss_energy, 16)
        pygame.draw.rect(SCREEN, 'teal', bar, border_radius=2)

    @staticmethod
    def draw_weapon():
        text_creator('Weapon', 'white', 162, 68, 29)
        weapon = pygame.image.load(Player.current_weapon)
        SCREEN.blit(weapon, (240, 38,))
        pygame.draw.rect(SCREEN, 'teal', [242, 54, 60, 24], 1, 2)

    @staticmethod
    def draw_amulet_bar():
        text_creator('Amulets', 'white', 240, 32, 29)
        # SCREEN.fill((70,70,70), [326, 15, 360, 40])
        [pygame.draw.rect(SCREEN, (200,220,222), [326 + 40 * n, 15, 40, 40], 1, 1,) for n in range(0, 9)]

    def update(self):
        self.get_current_area_level()
        self.create_top_frame()
        self.draw_lives()
        self.draw_top_score()
        self.draw_current_score()
        self.draw_area_and_level()
        self.energy_bar()
        # if game_state.boos_battle:
        self.energy_bar_boss()
        self.draw_weapon()
        self.draw_amulet_bar()
