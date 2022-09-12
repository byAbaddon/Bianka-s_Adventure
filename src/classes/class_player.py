import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH

vec = pygame.math.Vector2


# ============================================= class Player===============================================
class Player(pygame.sprite.Sprite):
    energy_power = 100
    player_dead = False
    counter = 0
    SPRITE_ANIMATION_SPEED = 0.2
    JUMP_HEIGHT = -8
    PLAYER_SPEED = 0.5
    PLAYER_FRICTION = -0.12
    game_timer = pygame.time.get_ticks()

    def __init__(self, all_sprite_groups_dict={}):
        pygame.sprite.Sprite.__init__(self)
        self.all_sprite_groups_dict = all_sprite_groups_dict
        self.sprites = [pygame.image.load(f'../src/assets/images/player/walking/{x}.png') for x in range(1, 7)]
        self.current_sprite = 0
        self.isAnimating = False
        self.image = self.sprites[self.current_sprite]
        self.player_height_size = self.image.get_height()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (SCREEN_WIDTH - 700, SCREEN_HEIGHT - self.player_height_size - 50)
        self.direction = 1  # stay 0; go right 1; -1 go left
        self.gravity = 0.3
        self.is_jump = False
        self.is_fail = False
        self.pos = vec(self.rect.x, self.rect.y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def movie_plyer(self):
        self.acceleration = vec(0, self.gravity)  # fail gravity

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.direction = 1
            self.acceleration.x = self.PLAYER_SPEED
        if key[pygame.K_LEFT]:
            self.direction = -1
            self.acceleration.x = -self.PLAYER_SPEED
        # jump
        if key[pygame.K_UP]:

            # self.is_jump = True
            # jump if player in the ground
            self.rect.y += 1
            hits_ground = pygame.sprite.spritecollide(self, self.all_sprite_groups_dict['ground'], False)
            self.rect.y -= 1
            if hits_ground:
                self.velocity.y = self.JUMP_HEIGHT
                # self.is_jump = False

        #     self.current_sprite += 0.1
        #     if self.direction == 1:
        #         self.image = pygame.image.load(f'assets/images/player/jump/2.png')
        #     if self.direction == -1:
        #         self.image = pygame.transform.flip(pygame.image
        #                                            .load(f'assets/images/player/jump/2.png'), True, False)
        #     if self.direction == 0:
        #         self.image = pygame.image.load('assets/images/player/jump/1.png')

        # apply friction
        self.acceleration.x += self.velocity.x * self.PLAYER_FRICTION
        # equations of motion
        self.velocity += self.acceleration
        self.pos += self.velocity + self.acceleration * 0.5
        self.rect.midbottom = self.pos

        if key[pygame.K_RIGHT] or key[pygame.K_LEFT]:
            self.isAnimating = True

        # shooting
        if key[pygame.K_SPACE]:
            self.shooting_bullet_position()

    def sprite_frames(self):
        if self.isAnimating:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 1
            self.image = self.sprites[int(self.current_sprite)]

    def flip_image(self):
        if self.direction == -1 and self.isAnimating:  # go to left
            self.image = pygame.transform.flip(self.image, True, False)
        self.isAnimating = False

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
                if hits[0].rect.top:
                    self.pos.y = hits[0].rect.top + buffer  # +3 buffer after collide for removing player trembling
                    self.velocity.y = 0

    def update(self):
        pygame.mask.from_surface(self.image)  # create mask image
        self.sprite_frames()
        self.flip_image()
        self.movie_plyer()
        self.check_ground_collide()
