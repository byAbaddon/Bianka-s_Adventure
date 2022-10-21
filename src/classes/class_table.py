from src.settings import *


class Table:
    height_score = 3000
    boss_energy = 200
    energy_power = 100
    area = 0
    level = 0
    score = 0
    lives = 0
    weapon = 'knife'
    is_poisoned = False

    def __init__(self, game_state, player, knight):
        self.game_state = game_state
        self.player = player
        self.knight = knight

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
        # todo: draw original 4 levels before increase area
        # text_creator(f'Area:  {self.area}', (255, 200, 0), SCREEN_WIDTH - 92, 24, 29)
        # if not self.player.is_boos_level:
        #     text_creator(f'Level: {self.level}', (255, 200, 0), SCREEN_WIDTH - 92, 44, 29)
        # else:
        #     text_creator(f'-BOSS-', (255, 200, 0), SCREEN_WIDTH - 92, 44, 29)
        #
        text_creator(f'Level: {self.level}', (255, 200, 0), SCREEN_WIDTH - 94, 24, 29)
        if not self.player.is_boss_level:
            text_creator(f'Area:  {self.area}', (255, 200, 0), SCREEN_WIDTH - 92, 44, 29)
        else:
            text_creator(f'-BOSS-', (255, 200, 0), SCREEN_WIDTH - 92, 44, 29)

    def energy_bar(self):
        text_creator('Bianka', 'white', 328, 67, 29)
        # bottom bar red
        bar = pygame.Rect(400, 60, 100, 16)
        pygame.draw.rect(SCREEN, 'red', bar, border_radius=2)

        # top bar green / blue
        bar = pygame.Rect(400, 60, self.energy_power, 16)
        # is_poisoned
        if self.is_poisoned:
            pygame.draw.rect(SCREEN, (147, 112, 219), bar, border_radius=1)  # up purple
        else:
            pygame.draw.rect(SCREEN, (0, 200, 0), bar, border_radius=2)  # up green

    def energy_bar_boss(self):
        text_creator('Boss', 'white', 527, 67, 29)
        # bottom red
        bar = pygame.Rect(SCREEN_WIDTH - 219, 60, 200, 16)
        pygame.draw.rect(SCREEN, 'red', bar, border_radius=2)
        # up blue
        bar = pygame.Rect(SCREEN_WIDTH - 219, 60, self.boss_energy, 16)
        pygame.draw.rect(SCREEN, 'teal', bar, border_radius=2)

    def draw_weapon(self):
        text_creator('Weapon', 'white', 162, 68, 29)
        weapon = pygame.image.load(self.player.current_weapon)
        SCREEN.blit(weapon, (244, 38,))
        pygame.draw.rect(SCREEN, 'teal', [246, 54, 60, 24], 1, 2)

    def draw_amulet_bar(self):
        text_creator('Amulets', 'white', 240, 32, 29)

        # draw cells
        # SCREEN.fill((70,70,70), [326, 15, 360, 40])
        [pygame.draw.rect(SCREEN, (200, 220, 222), [326 + 40 * x, 15, 40, 40], 1, 1,) for x in range(0, 9)]

        # draw items
        # if self.player.is_player_kill_boss:
        for x in range(0, self.level - 1):
            pic = pygame.image.load(self.player.AMULETS_LIST[x])
            SCREEN.blit(pic, [332 + (41 * x - 1) - (x + 2), 18,  36, 36])

    def updated_player_data(self):
        self.area = self.game_state.area
        self.level = self.game_state.level
        self.score = self.player.points
        self.lives = self.player.lives
        self.energy_power = self.player.energy_power
        self.weapon = self.player.current_weapon
        self.is_poisoned = self.player.is_player_poisoned
        self.boss_energy = self.knight.energy_power

    def update(self):
        self.create_top_frame()
        self.draw_lives()
        self.draw_top_score()
        self.draw_current_score()
        self.draw_area_and_level()
        self.energy_bar()
        # if game_state.boos_battle:a
        self.energy_bar_boss()
        self.draw_weapon()
        self.draw_amulet_bar()
        self.updated_player_data()



