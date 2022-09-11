import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


# ============================================= class Player===============================================
class Player(pygame.sprite.Sprite):
    energy_power = 100
    player_dead = False
    counter = 0
    SPRITE_ANIMATION_SPEED = 0.2
    PLAYER_HEIGHT_SIZE = 134 - 4
    PLAYER_SPEED = 4
    ACCELERATION = 6
    JUMP_HEIGHT = 20

    def __init__(self, x=SCREEN_WIDTH - 700, y=SCREEN_HEIGHT - 330):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load(f'../src/assets/images/player/walking/{x}.png') for x in range(1, 7)]
        self.current_sprite = 0
        self.isAnimating = False
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (x, y)
        self.rect.midbottom = self.rect.center
        self.direction = 1  # stay 0; go right 1; -1 go left
        self.gravity = 5
        self.is_jump = False

    def movie_plyer(self):
        key = pygame.key.get_pressed()
        # fail gravity
        self.rect.y += self.gravity
        if self.gravity == 0:
            self.is_jump = False

        if not self.is_jump:
            if key[pygame.K_RIGHT]:
                self.direction = 1
                self.rect.x += self.PLAYER_SPEED
            if key[pygame.K_LEFT]:
                self.direction = -1
                self.rect.x -= self.PLAYER_SPEED

            if key[pygame.K_RIGHT] or key[pygame.K_LEFT]:
                self.isAnimating = True
        # jump
        if key[pygame.K_UP]:
            self.is_jump = True
            self.rect.y -= self.JUMP_HEIGHT

            self.current_sprite += 0.1
            if self.direction == 1:
                self.rect.x += self.ACCELERATION
                self.image = pygame.image.load(f'assets/images/player/jump/2.png')
            if self.direction == -1:
                self.rect.x -= self.ACCELERATION
                self.image = pygame.transform.flip(pygame.image
                                                   .load(f'assets/images/player/jump/2.png'), True, False)
            if self.direction == 0:
                self.image = pygame.image.load('assets/images/player/jump/1.png')

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

    def update(self):
        pygame.mask.from_surface(self.image)  # create mask image
        self.sprite_frames()
        self.flip_image()
        self.movie_plyer()


# ============================================= class Ground=============================================
class Ground(pygame.sprite.Sprite):
    def __init__(self, picture='../src/assets/images/ground/gr_1.png',  x=0, y=SCREEN_HEIGHT - 78):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picture).convert()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.x = x
        self.rect.y = y


# ============================================= class Bullet=============================================
class Bullet(pygame.sprite.Sprite):
    BULLED_SPEED = 6

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.rotation = 0
        self.image = pygame.image.load('assets/images/bullets/spear_90.png')
        self.rect = self.image.get_rect(center=pos)
        self.position = pos
        self.direction = 1

    def update(self):
        pygame.mask.from_surface(self.image)  # create mask image
        # self.position += self.direction  # Update the position vector.
        self.rect.center = self.position  # Update the position rect.

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT:
            self.kill()  # remove old shot from bullets_group

