import pygame
import random
import os
import sys

all_sprites = pygame.sprite.Group()
circles = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
colors = ['red',
          'green', 'blue', 'yellow', 'purple', 'black', 'orange', 'cyan', 'brown']


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(circles)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color(colors[random.randint(0, len(colors) - 1)]),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
            self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
            self.rect = self.rect.move(self.vx, self.vy)

        circles.remove(self)
        curcircle = pygame.sprite.Group(self)
        if pygame.sprite.spritecollideany(self, circles):
            print(pygame.sprite.groupcollide(curcircle, circles, False, False)[self])
            for i in pygame.sprite.groupcollide(curcircle, circles, False, False)[self]:
                i.vx, i.vy, self.vx, self.vy = self.vx, self.vy, i.vx, i.vy
                i.rect = i.rect.move(i.vx, i.vy)
                self.rect = self.rect.move(self.vx, self.vy)
        curcircle.empty()
        circles.add(self)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


if __name__ == '__main__':
    pygame.init()
    width = 500
    height = 500
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    Balls = []
    for i in range(10):
        Balls.append(Ball(20, random.randint(30, height - 30), random.randint(30, height - 30)))
    for i in circles:
        print(i)
    running = True
    while running:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
