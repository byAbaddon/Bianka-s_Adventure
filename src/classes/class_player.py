import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH

vec = pygame.math.Vector2


# ============================================= class Player===============================================
class Player(pygame.sprite.Sprite):
    energy_power = 100
    player_dead = False
    counter = 0
    COOLDOWN = 300  # milliseconds
    GRAVITY = 0.3
    SPRITE_ANIMATION_SPEED = 0.2
    JUMP_HEIGHT = -8
    PLAYER_SPEED = 0.5
    PLAYER_FRICTION = -0.12

    def __init__(self, all_sprite_groups_dict={}):
        pygame.sprite.Sprite.__init__(self)
        self.all_sprite_groups_dict = all_sprite_groups_dict
        self.image = self.image = pygame.image.load('../src/assets/images/player/stay/1_right.png')
        self.sprites = [pygame.image.load(f'../src/assets/images/player/walking/{x}.png') for x in range(1, 7)]
        self.current_sprite = 0
        self.isAnimating = False
        self.player_height_size = self.image.get_height()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (SCREEN_WIDTH - 700, SCREEN_HEIGHT - self.player_height_size - 50)
        self.is_jump = False
        self.is_fail = False
        self.direction = vec(0, 0)  # stay 0; -1 go left; right 1; down 1 ; up -1
        self.pos = vec(self.rect.x, self.rect.y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.last_timer = pygame.time.get_ticks()
        self.time_now = 0

    def movie_plyer(self):
        self.acceleration = vec(0, self.GRAVITY)  # fail gravity
        self.direction = vec(self.direction.x, self.direction.y)

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.direction.y == 1:
            self.direction = vec(1, 0)
            self.acceleration.x = self.PLAYER_SPEED
        if key[pygame.K_LEFT] and self.direction.y == 1:
            self.direction = vec(-1, 0)
            self.acceleration.x = -self.PLAYER_SPEED
        # jump
        if key[pygame.K_UP] and self.direction.y == 1:
            # jump if player in the ground
            # self.rect.y += 1
            hits_ground = pygame.sprite.spritecollide(self, self.all_sprite_groups_dict['ground'], False)
            # self.rect.y -= 1
            if hits_ground:
                self.direction.y = -1
                self.velocity.y = self.JUMP_HEIGHT

        # apply friction
        self.acceleration.x += self.velocity.x * self.PLAYER_FRICTION
        # equations of motion
        self.velocity += self.acceleration
        self.pos += self.velocity + self.acceleration * 0.5
        self.rect.midbottom = self.pos

        # shooting
        if key[pygame.K_SPACE]:
            self.shooting_bullet_position()

    def sprite_frames(self):
        self.current_sprite += self.SPRITE_ANIMATION_SPEED
        if self.direction.y == 1 and pygame.key.get_pressed():
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 1
            self.image = self.sprites[int(self.current_sprite)]
        # if self.direction.y == 1 and self.direction.x == 1:
        #     self.image = pygame.image.load('../src/assets/images/player/jump/3.png')
        # if self.direction.y == 0:
        #     self.image = pygame.image.load('../src/assets/images/player/jump/1.png')

    def flip_image(self):
        if self.direction.x == -1 and self.direction.y == 1:  # go to left
            self.image = pygame.transform.flip(self.image, True, False)
        # if self.direction.x == -1:
        #     self.image = pygame.transform.flip(pygame.image
        #                                        .load('../src/assets/images/player/jump/2.png'), True, False)

    #  shooting bullets
    def shooting_bullet_position(self):
        return self.rect.center

    def check_ground_collide(self):
        buffer = 5  # buffer image to improve collide
        # ground and player collide
        hits = pygame.sprite.spritecollide(self, self.all_sprite_groups_dict['ground'], False)
        if hits:
            # check_ground_border
            hits_ground = hits[0]
            if not (hits_ground.rect.left > self.pos.x or self.pos.x > hits_ground.rect.right):
                # ground collide
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top + buffer  # buffer after collide for removing player trembling
                    self.velocity.y = 0
                    self.direction.y = 1

    def update(self):
        pygame.mask.from_surface(self.image)  # create mask image
        self.sprite_frames()
        self.flip_image()
        self.movie_plyer()
        self.check_ground_collide()
        self.time_now = pygame.time.get_ticks()
