import pygame
from pygame import *
import random
import os
import sys

lifes = 3
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


def load_image(name):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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
        self.vx = random.randint(-1, 1)
        while self.vx == 0:
            self.vx = random.randint(-1, 1)

        self.vy = random.randint(-1, 1)
        while self.vy == 0:
            self.vy = random.randint(-1, 1)

    def update(self):

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


class Main_char(Ball):
    def __init__(self):
        super().__init__(15, width // 2 - 15, height // 2 - 15)
        self.add(main_character)
        pygame.draw.circle(self.image, pygame.Color('yellow'),
                           (self.radius, self.radius), self.radius)
        self.vx = 1
        self.vy = 1

        self.last_touch = pygame.time.get_ticks()

    def update(self):
        if pygame.sprite.spritecollideany(self, enemy_circles) and (
                pygame.time.get_ticks() - self.last_touch) / 1000 >= 2.5:
            global lifes
            lifes -= 1
            self.last_touch = pygame.time.get_ticks()

    def up(self):
        self.rect = self.rect.move(0, -self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, self.vy)

    def down(self):
        self.rect = self.rect.move(0, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, -self.vy)

    def left(self):
        self.rect = self.rect.move(-self.vx, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(self.vx, 0)

    def right(self):
        self.rect = self.rect.move(self.vx, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(-self.vx, 0)


class Healthbar():
    def __init__(self):
        self.image = load_image('Heart.png').convert_alpha()
        # if height * width <= 921600:
        #self.image = pygame.transform.scale(self.image, (width // 15, height // 15))

    def update(self):
        global lifes
        if height * width <= 921600:
            self.image = pygame.transform.scale(self.image, (width // 15, height// 15))
            for i in range(lifes):
                screen.blit(self.image, (width // 20 + (i * width // 15), height // 20))
        else:
            for i in range(lifes):
                screen.blit(self.image, (width // 20 + (i * width // 35), height // 20))


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
        Enemy_balls.append(
            Enemy(random.randint(15, 20), random.randint(50, width - 50), random.randint(50, height - 50)))
    for i in range(width * height // 10000):
        Stars(random.randint(50, width - 50), random.randint(50, height - 50))
    main_char = Main_char()
    healthbar = Healthbar()
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
                main_char.kill()
                main_character.empty()
                main_char = Main_char()

                for i in enemy_circles:
                    i.kill()
                for i in stars:
                    i.kill()
                enemy_circles.empty()
                stars.empty()
                for i in range(width * height // 72000):
                    Enemy_balls.append(
                        Enemy(random.randint(15, 20), random.randint(0, width), random.randint(0, height)))

                for i in range(width * height // 10000):
                    Stars(random.randint(0, width), random.randint(0, height))
                horizontal_borders.empty()
                vertical_borders.empty()
                Border(5, 5, width - 5, 5)
                Border(5, height - 5, width - 5, height - 5)
                Border(5, 5, 5, height - 5)
                Border(width - 5, 5, width - 5, height - 5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            main_char.left()
        elif keys[pygame.K_RIGHT]:
            main_char.right()
        if keys[pygame.K_UP]:
            main_char.up()
        elif keys[pygame.K_DOWN]:
            main_char.down()

        healthbar.update()
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(300)
    pygame.quit()
