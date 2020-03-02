import pygame as pg
from pygame.math import Vector2


class Entity(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((50, 30), pg.SRCALPHA)  # A transparent image.
        # Draw a triangle onto the image.
        pg.draw.polygon(self.image, pg.Color('dodgerblue2'),
                        ((0, 0), (50, 15), (0, 30)))
        # A reference to the original image to preserve the quality.
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)
        self.gol = (300, 300)

    def update(self, *args):
        # Subtract the pos vector from the mouse pos to get the heading,
        # normalize this vector and multiply by the desired speed.
        # self.vel = (pg.mouse.get_pos() - self.pos).normalize() * 5

        if args and args[0] is not None:

            if args[0].key == pg.K_w:
                self.vel = (((self.rect.topright[0] - self.rect.x) // 2 + self.rect.x,
                             self.rect.top) - self.pos).normalize() * 5
                self.pos += self.vel    
                self.rect.center = self.pos
            if args[0].key == pg.K_SPACE:
                pass
            if args[0].key == pg.K_s:
                self.vel = (((self.rect.topright[0] - self.rect.x) // 2 + self.rect.x,
                             self.rect.top) - self.pos).normalize() * 5
                self.pos -= self.vel
                self.rect.center = self.pos

            if args[0].key == pg.K_d:
                radius, angle = self.vel.as_polar()
            if args[0].key == pg.K_a:
                pass
        # Update the position vector and the rect.
        # self.pos += self.vel
        # self.rect.center = self.pos

        # Rotate the image.
        # 'Vector2.as_polar' returns the polar coordinates (radius and angle).
        radius, angle = self.vel.as_polar()
        # self.image = pg.transform.rotozoom(self.orig_image, -angle, 1)
        # self.rect = self.image.get_rect(center=self.rect.center)


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    entity = Entity((100, 300), all_sprites)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                all_sprites.update(event)

        screen.fill((30, 30, 30))
        all_sprites.update(None)
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
