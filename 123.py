import pygame
from pygame.locals import *


def rotate(img, pos, angle):
    w, h = img.get_size()
    img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
    img2.blit(img, (w - pos[0], h - pos[1]))
    return pygame.transform.rotate(img2, angle)


pygame.init()
screen = pygame.display.set_mode([640, 480])
screen.fill((135, 206, 250))
pygame.display.set_caption("Вращение")

imagec = pygame.image.load("gun.jpg").convert_alpha()
pivot = (200, 200)  # положение центра вращения на экране
angle = 0
center_image = (200, 100)  # положение центра вращения на изображении

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((135, 206, 250))

    image = rotate(imagec, center_image, angle)
    rect = image.get_rect()
    rect.center = pivot
    screen.blit(image, rect)

    angle += 1 % 360

    pygame.display.update()

pygame.quit()