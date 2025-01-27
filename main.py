import pygame
from pygame import *
import random
import os
import sys

lifes = 3
width = 600
height = 600
point_balls_count = 0
points = 0
all_sprites = pygame.sprite.Group()
main_character = pygame.sprite.Group()
enemy_circles = pygame.sprite.Group()
point_circles = pygame.sprite.Group()
stars = pygame.sprite.Group()
circles = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


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
    def __init__(self):
        super().__init__(1, random.randint(50, width - 50), random.randint(50, width - 50))
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
        self.v = 1

        self.last_touch = pygame.time.get_ticks()

    def update(self):
        if pygame.sprite.spritecollideany(self, enemy_circles) and (
                pygame.time.get_ticks() - self.last_touch) / 1000 >= 1.5:
            global lifes
            lifes -= 1
            self.last_touch = pygame.time.get_ticks()

    def up(self, v):
        self.v = v
        self.rect = self.rect.move(0, -self.v)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, self.v)

    def down(self, v):
        self.v = v
        self.rect = self.rect.move(0, self.v)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, -self.v)

    def left(self, v):
        self.v = v
        self.rect = self.rect.move(-self.v, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(self.v, 0)

    def right(self, v):
        self.v = v
        self.rect = self.rect.move(self.v, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(-self.v, 0)


class Healthbar():
    def __init__(self):
        self.image = load_image('Heart.png').convert_alpha()

    def update(self):
        global lifes
        if height * width <= 921600:
            self.image = pygame.transform.scale(self.image, (width // 15, height // 15))
            for i in range(lifes):
                screen.blit(self.image, (width // 20 + (i * width // 15), height // 20))
        else:
            for i in range(lifes):
                screen.blit(self.image, (width // 20 + (i * width // 35), height // 20))


class Pointballs(Ball):
    def __init__(self):
        super().__init__(5, random.randint(50, width - 50), random.randint(50, width - 50))
        self.add(point_circles)
        pygame.draw.circle(self.image, pygame.Color('orange'),
                           (self.radius, self.radius), self.radius)

    def update(self):
        if pygame.sprite.spritecollideany(self, main_character):
            global points, point_balls_count
            points += 1
            point_balls_count -= 1
            self.kill()


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


def main():
    global running, main_char, width, height, screen, clock, point_balls_count, points
    screen.fill('black')
    text_surface = fnt.render(f'Текущий счет: {points}', True, (255, 255, 255))
    screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, 5))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width, height = event.w, event.h
            update()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (
            keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
        main_char.left(2)
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (
            keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
        main_char.left(1)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (
            keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
        main_char.right(2)
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (
            keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
        main_char.right(1)
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not (
            keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a]):
        main_char.up(2)
    elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (
            keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a]):
        main_char.up(1)
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not (
            keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a]):
        main_char.down(2)
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (
            keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a]):
        main_char.down(1)

    if point_balls_count <= 0:
        for j in point_circles:
            j.kill()
        point_circles.empty()
        for i in range(width * height // 30000):
            Point_Balls.append(Pointballs())
            point_balls_count += 1
    healthbar.update()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(200)


def update():
    global running, points, enemy_circles, main_char, width, height, point_balls_count
    Enemy_balls.clear()
    Point_Balls.clear()
    main_char.kill()
    main_character.empty()
    main_char = Main_char()
    for j in point_circles:
        j.kill()
    for j in enemy_circles:
        j.kill()
    for j in stars:
        j.kill()
    point_circles.empty()
    enemy_circles.empty()
    stars.empty()
    for j in range(width * height // 72000):
        Enemy_balls.append(
            Enemy(random.randint(15, 20), random.randint(0, width), random.randint(0, height)))
    for j in range(width * height // 10000):
        Stars()
    for j in range(width * height // 30000):
        Point_Balls.append(Pointballs())
        point_balls_count += 1
    horizontal_borders.empty()
    vertical_borders.empty()
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)


def death_screen():
    global screen, width, height
    text = ["Вы проиграли :(", f'Ваш счет - {points}', 'Щелкните мышкой чтобы продолжить']
    font = pygame.font.Font(None, 30)
    screen.fill('black')
    for i in range(len(text)):
        text_surface = font.render(text[i], True, pygame.Color('white'))
        screen.blit(text_surface,
                    (width // 2 - text_surface.get_width() // 2, height // 2 - len(text) * 30 // 2 + i * 30))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width, height = event.w, event.h
                update()
                for i in range(len(text)):
                    text_surface = font.render(text[i], True, pygame.Color('white'))
                    screen.blit(text_surface,
                                (
                                    width // 2 - text_surface.get_width() // 2,
                                    height // 2 - len(text) * 30 // 2 + i * 30))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    size = width, height
    screen = pygame.display.set_mode(size, RESIZABLE)
    clock = pygame.time.Clock()
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    Enemy_balls = []
    Stars_arr = []
    Point_Balls = []
    for i in range(width * height // 72000):
        Enemy_balls.append(
            Enemy(random.randint(15, 20), random.randint(50, width - 50), random.randint(50, height - 50)))
    for i in range(width * height // 10000):
        Stars()
    for i in range(width * height // 30000):
        Point_Balls.append(Pointballs())
        point_balls_count += 1

    main_char = Main_char()
    healthbar = Healthbar()
    fnt = pygame.font.Font(None, 32)
    text_surface = fnt.render(f'Текущий счет: {points}', True, (255, 255, 255))
    screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, 5))
    running = True
    start_tick = None
    while running:
        main()
        if lifes <= 0:
            text_surface = fnt.render(f'Текущий счет: {points}', True, (255, 255, 255))
            screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, 5))
            if death_screen():
                running = True
                lifes = 3
                point_balls_count = 0
                points = 0
                update()

    pygame.quit()
    sys.exit()
