import pygame
from pygame import *
import random
import os
import sys

all_sprites = pygame.sprite.Group()
main_character = pygame.sprite.Group()
enemy_circles = pygame.sprite.Group()
point_circles = pygame.sprite.Group()
stars = pygame.sprite.Group()
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

        self.vy = random.randint(-2, 2)
        while self.vy == 0:
            self.vy = random.randint(-2, 2)

    def update(self):
        # self.rect = self.rect.move(self.vx, self.vy)

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
        curcircle.empty()
        circles.add(self)
        # if self.rect.x >= width or self.rect.y >= height or self.rect.x <= 0 or self.rect.y <= 0:
        #    self.rect = pygame.Rect(random.randint(30, width - 30), random.randint(30, width - 30), 2 * self.radius,
        #                            2 * self.radius)
        if self.rect.x <= 0:
            self.rect.x = 50
        if self.rect.y <= 0:
            self.rect.y = 50
        if self.rect.x >= width:
            self.rect.x = width - 50
        if self.rect.y >= height:
            self.rect.y = height - 50


class Stars(Ball):
    def __init__(self, x, y):
        super().__init__(1, x, y)
        self.add(stars)
        pygame.draw.circle(self.image, pygame.Color('white'),
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(random.randint(0, width), random.randint(0, height), 1, 1)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([0, y2 - y1])
            self.rect = None
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 0])
            self.rect = None
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


if __name__ == '__main__':
    pygame.init()
    width = 600
    height = 600
    size = width, height
    screen = pygame.display.set_mode(size, RESIZABLE)
    clock = pygame.time.Clock()
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    Enemy_balls = []
    Stars_arr = []
    for i in range(width * height // 72000):
        Enemy_balls.append(Enemy(20, random.randint(50, width - 50), random.randint(50, height - 50)))
    for i in range(width * height // 10000):
        Stars(random.randint(50, width - 50), random.randint(50, height - 50))
    running = True
    while running:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                width, height = event.w, event.h
                Enemy_balls.clear()
                for i in enemy_circles:
                    i.kill()
                for i in stars:
                    i.kill()
                enemy_circles.empty()
                stars.empty()
                for i in range(width * height // 72000):
                    Enemy_balls.append(Enemy(20, random.randint(0, width), random.randint(0, height)))

                for i in range(width * height // 10000):
                    Stars(random.randint(0, width), random.randint(0, height))
                horizontal_borders.empty()
                vertical_borders.empty()
                Border(5, 5, width - 5, 5)
                Border(5, height - 5, width - 5, height - 5)
                Border(5, 5, 5, height - 5)
                Border(width - 5, 5, width - 5, height - 5)

        # for i in range(width * height // 70000):
        #    star = pygame.draw.rect(screen, 'white', (random.random() * width, random.random() * height, 1, 1))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(120)
    pygame.quit()
