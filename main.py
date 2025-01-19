import pygame
import random
import os
import sys

all_sprites = pygame.sprite.Group()
main_character = pygame.sprite.Group()
enemy_circles = pygame.sprite.Group()
point_circles = pygame.sprite.Group()
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
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)


class Enemy(Ball):
    def __init__(self, radius, x, y):
        super().__init__(radius, x, y)
        self.add(enemy_circles)
        pygame.draw.circle(self.image, pygame.Color('red'),
                           (radius, radius), radius)
        self.vx = random.randint(-2, 2)
        while self.vx == 0:
            self.vx = random.randint(-2, 2)

        self.vy = random.randrange(-2, 2)
        while self.vy == 0:
            self.vy = random.randrange(-2, 2)

    def update(self):
        #self.rect = self.rect.move(self.vx, self.vy)

        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
            self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
            self.rect = self.rect.move(self.vx, self.vy)
        self.rect = self.rect.move(self.vx, self.vy)
        circles.remove(self)
        curcircle = pygame.sprite.Group(self)
        if pygame.sprite.spritecollideany(self, enemy_circles):
            for i in pygame.sprite.groupcollide(curcircle, enemy_circles, False, False)[self]:
                i.vx, i.vy, self.vx, self.vy = self.vx, self.vy, i.vx, i.vy
                #if not (
                #        pygame.sprite.spritecollideany(self, horizontal_borders)
                #        or pygame.sprite.spritecollideany(self, vertical_borders)):
                #    i.rect = i.rect.move(i.vx, i.vy)
                #    self.rect = self.rect.move(self.vx, self.vy)
        curcircle.empty()
        circles.add(self)
        # if pygame.sprite.spritecollideany(self, enemy_circles) and not (
        #        pygame.sprite.spritecollideany(self, horizontal_borders)
        #        or pygame.sprite.spritecollideany(self, vertical_borders)):
        #    self.rect = self.rect.move(self.vx, self.vy)


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
    width = 1240
    height = 960
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    Enemy_balls = []
    for i in range(5):
        Enemy_balls.append(Enemy(20, random.randint(20, width - 20), random.randint(20, height - 20)))
    running = True
    while running:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
