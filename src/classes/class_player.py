import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, vec


# ============================================= class Player===============================================
class Player(pygame.sprite.Sprite):
    COOLDOWN = 1000  # milliseconds
    GRAVITY = 0.2
    SPRITE_ANIMATION_SPEED = 0.3
    JUMP_HEIGHT = -6
    PLAYER_FRICTION = -0.12
    PLAYER_SPEED = 0.4
    energy_power = 100
    player_dead = False
    counter = 0

    def __init__(self, class_bullet, all_sprite_groups_dict={}):
        pygame.sprite.Sprite.__init__(self)
        self.class_bullet = class_bullet
        self.all_sprite_groups_dict = all_sprite_groups_dict
        self.image = self.image = pygame.image.load('../src/assets/images/player/stay/1.png')
        self.sprites_walking = [pygame.image.load(f'../src/assets/images/player/walking/{x}.png') for x in range(1, 7)]
        self.current_sprite = 0
        self.player_height_size = self.image.get_height()
        self.player_width_size = self.image.get_width()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (SCREEN_WIDTH - 700, SCREEN_HEIGHT - (self.player_height_size - 124))
        self.is_jump = False
        self.direction = vec(0, 1)  # stay 0
        self.pos = vec(self.rect.x, self.rect.y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.last_time = pygame.time.get_ticks()
        self.shot_position = self.pos
        self.WALK_LEFT_SCREEN_BORDER = self.player_width_size - 14
        self.WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH // 3

    def movie_plyer(self):
        self.acceleration = vec(0, self.GRAVITY)  # fail gravity
        self.direction = vec(self.direction.x, self.direction.y)

        key = pygame.key.get_pressed()

        # jump up
        if key[pygame.K_UP] and self.direction.y == 1 and self.direction.x != 0:
            self.is_jump = True
            self.direction.y = -1
            self.velocity.y = self.JUMP_HEIGHT
            if self.direction.x == 1:
                self.image = pygame.image.load('../src/assets/images/player/jump/2.png')
            else:
                self.image = pygame.transform.flip(
                    pygame.image.load('../src/assets/images/player/jump/2.png'), True, False)
            # change image if player jump in Right Boreder
            if self.pos.x >= self.WALK_LEFT_SCREEN_BORDER and key[pygame.K_RIGHT]:
                self.image = pygame.image.load('../src/assets/images/player/walking/5.png')

        # jump up right
        if key[pygame.K_UP] and key[pygame.K_RIGHT] and self.pos.x < self.WALK_RIGHT_SCREEN_BORDER:
            if not self.is_jump:
                self.velocity.y = self.JUMP_HEIGHT
            self.direction = vec(1, 0)
            self.acceleration.x = self.PLAYER_SPEED
            self.is_jump = True
            self.image = pygame.image.load('../src/assets/images/player/walking/5.png')

        # jump up left
        if key[pygame.K_UP] and key[pygame.K_LEFT] and self.pos.x >= self.WALK_LEFT_SCREEN_BORDER:
            if self.pos.x <= 80:
                self.direction.x = 1
            else:
                self.direction.x = -1
            if not self.is_jump:
                self.velocity.y = self.JUMP_HEIGHT
            self.acceleration.x = -self.PLAYER_SPEED
            self.is_jump = True
            self.image = pygame.transform.flip(
                pygame.image.load('../src/assets/images/player/walking/5.png'), True, False)

        # go left
        if key[pygame.K_LEFT] and self.direction.y == 1 and self.pos.x >= self.WALK_LEFT_SCREEN_BORDER:
            if self.pos.x <= 80:
                self.direction.x = 1
            else:
                self.direction.x = -1
            self.acceleration.x = -self.PLAYER_SPEED
            self.image = pygame.transform.flip(self.image, True, False)

        # go right
        if key[pygame.K_RIGHT] and self.direction.y == 1 and self.pos.x <= self.WALK_RIGHT_SCREEN_BORDER:
            self.direction.x = 1
            self.acceleration.x = self.PLAYER_SPEED

        # running
        # if key[pygame.K_a] and self.pos.x > self.WALK_LEFT_SCREEN_BORDER:
        #     if not self.direction.y == -1 and not self.direction.y == 0:
        #         if self.direction.x == 1:
        #             self.velocity.x += 0.5
        #         elif self.direction.x == -1:
        #             self.velocity.x -= 0.5

        # shooting
        time_now = pygame.time.get_ticks()  # get time now
        # velocity is equal shooting window time
        if key[pygame.K_s] and self.direction.x != 0 \
                and abs(self.velocity.x) <= 3.0 and time_now - self.last_time > self.COOLDOWN:
            self.last_time = time_now

            self.shot_position = self.rect.midright
            y = self.shot_position[1] - 26

            if self.direction.x == 1:
                x = self.shot_position[0] + 30
                self.image = pygame.image.load('../src/assets/images/player/angry/1.png')
            else:
                self.image = pygame.image.load('../src/assets/images/player/angry/2.png')
                x = self.shot_position[0] - 104

            bullet = self.class_bullet(x, y, self.direction)
            self.all_sprite_groups_dict['bullets'].add(bullet)

        # =============================================================== MOVEMENT !!!
        # apply friction
        self.acceleration.x += self.velocity.x * self.PLAYER_FRICTION
        # equations of motion
        self.velocity += self.acceleration
        # set velocity in zero if player no movement
        # if abs(self.velocity.x) < 0.1:
        #     self.velocity.x = 0
        # player running
        self.pos += self.velocity + self.acceleration * self.PLAYER_SPEED
        self.rect.midbottom = self.pos
        # ============================================================================

    def sprite_frames(self):
        key = pygame.key.get_pressed()
        # left and right animation
        if self.direction.y == 1 and (key[pygame.K_LEFT] or (key[pygame.K_RIGHT]) or
                                      (self.pos.x >= self.WALK_RIGHT_SCREEN_BORDER) and key[pygame.K_RIGHT]):
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites_walking):
                self.current_sprite = 1
            self.image = self.sprites_walking[int(self.current_sprite)]

    def check_ground_collide(self):
        buffer = 5  # buffer image to improve collide
        # ground and player collide
        hits = pygame.sprite.spritecollide(self, self.all_sprite_groups_dict['ground'], False)
        if hits:
            # check_ground_border
            hits_ground = hits[0]
            if not (hits_ground.rect.left > self.pos.x or self.pos.x > hits_ground.rect.right):
                # check is player head hits in bottom platform
                if self.pos.y < hits[0].rect.bottom:
                    # ground collide
                    self.pos.y = hits[0].rect.top + buffer  # buffer after collide for removing player trembling
                    self.velocity.y = 0
                    self.direction.y = 1

                    # change image after jump
                    if self.is_jump:
                        if self.direction.x == 1:
                            self.image = pygame.image.load('../src/assets/images/player/stay/1.png')
                        else:
                            self.image = pygame.transform.flip(
                                pygame.image.load('../src/assets/images/player/stay/1.png'), True, False)
                        self.is_jump = False

    def update(self):
        pygame.mask.from_surface(self.image)  # create mask image
        self.sprite_frames()
        self.movie_plyer()
        self.check_ground_collide()
