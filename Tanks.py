import sys

import pygame
from pygame.math import Vector2 as vec
import os

WIDTH = 1536
HEIGHT = 1024
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAX_SPEED = 5

START_CORDS = (300, 300)
MOVING = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen2 = pygame.Surface((186, 256))
X, Y = (300, 300)
pygame.display.set_caption('Tanks 2D')
clock = pygame.time.Clock()
screen.fill((0, 0, 0))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', *name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def rotate(img, angle):
    return pygame.transform.rotate(img, angle)


class Tank(pygame.sprite.Sprite):
    image = load_image(['Tank_1', 'Hull_01.png'], -1)
    center = (0, 0)
    top_left = (0, 0)
    top_right = (0, 0)
    ang = 0

    def __init__(self, group):
        super().__init__(group)
        self.image = Tank.image
        self.position = vec(300, 300)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.1)
        self.angle_speed = 0
        self.angle = 0
        self.update()

    def update(self, *args):
        global MOVING, Y, X
        Tank.center = self.rect.center
        Tank.top_left = self.rect.topleft
        Tank.top_right = self.rect.topright
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.angle_speed = 1
            self.rotate()
        if keys[pygame.K_a]:
            self.angle_speed = -1
            self.rotate()

        if keys[pygame.K_SPACE]:
            MOVING = False
            self.vel = vec(0, 0)

        if keys[pygame.K_w]:
            MOVING = True
            self.vel += self.acceleration

        if keys[pygame.K_s]:
            MOVING = True
            self.vel -= self.acceleration

        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        if MOVING:
            self.position += self.vel
            self.rect.center = self.position

    def rotate(self):
        # Rotate the acceleration vector.
        self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
            Tank.ang = -self.angle
        self.image = pygame.transform.rotate(Tank.image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Bashny(pygame.sprite.Sprite):
    image = load_image(['Tank_1', 'Gun_01.png'], -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Bashny.image
        self.rect = self.image.get_rect()
        self.rect.center = Tank.center
        self.angel = 0
        self.rotating = False
        self.angle_speed = 0
        self.angle = 0
        self.update()

    def update(self, *args):
        self.rect.center = Tank.center
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.angle_speed = 3
            self.rotate()
        if keys[pygame.K_LEFT]:
            self.angle_speed = -3
            self.rotate()

    def rotate(self):
        # Rotate the acceleration vector.
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(Bashny.image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # (Tank.center[0], Tank.center[1] + 44)


class Gusli(pygame.sprite.Sprite):
    images = [load_image(['Tank_1', 'tracks', 'Track_1_A.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_A.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_A.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_A.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_A.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_A.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_A.png'], -1),

              load_image(['Tank_1', 'tracks', 'Track_1_B.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_B.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_B.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_B.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_B.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_B.png'], -1),
              load_image(['Tank_1', 'tracks', 'Track_1_B.png'], -1),
              ]

    def __init__(self, group, left_or_right):
        super().__init__(group)
        self.side = left_or_right
        self.cur_frame = 0

        self.angle_speed = 0
        self.angle = 0

        self.image = Gusli.images[self.cur_frame]

        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        if self.side:
            self.rect.center = Tank.center[0] - 75, Tank.center[1] - 43
        else:
            self.rect.center = Tank.center[0] + 75, Tank.center[1] - 43
        if MOVING:
            self.cur_frame = (self.cur_frame + 1) % len(Gusli.images)
            self.image = Gusli.images[self.cur_frame]

    def rotate(self):
        # Rotate the acceleration vector.
        self.angle = Tank.ang
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Tires(pygame.sprite.Sprite):
    image = load_image(['Tank_1', 'Tire_Track_02.png'], -1)

    def __init__(self, group, left_or_right):
        super().__init__(group)
        self.image = Tires.image
        self.rect = self.image.get_rect()
        self.side = left_or_right
        self.update()

    def update(self):
        global MOVING
        self.rect = self.image.get_rect()
        if MOVING:
            if self.side:
                self.rect.x, self.rect.y = Gusli.right_cord[0], Gusli.right_cord[1] + 256
            else:
                self.rect.x, self.rect.y = Gusli.left_cord[0], Gusli.left_cord[1] + 256
        else:
            self.kill()


all_sprites = pygame.sprite.Group()
t = Tank(all_sprites)
b = Bashny(all_sprites)

gus = pygame.sprite.Group()

g_l = Gusli(gus, False)
g_r = Gusli(gus, True)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                all_sprites.update()
            if event.type == pygame.KEYUP:
                Tank.update(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        # ----
        screen.fill(WHITE)
        gus.draw(screen)
        all_sprites.draw(screen)
        # screen.blit(screen2, (X, Y))
        # screen2.fill((0, 0, 0))
        gus.update()
        all_sprites.update()

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main()
