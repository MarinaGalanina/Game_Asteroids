import random
import pygame
import os

WIDTH, HEIGHT = 720, 720

SMALL_ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join("PICS", "asteroid1.png")),
                                        (int(WIDTH / 20), int(HEIGHT / 20)))
MEDIUM_ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join("PICS", "asteroid2.png")),
                                         (int(WIDTH / 11), int(HEIGHT / 11)))
HUGE_ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join("PICS", "asteroid3.png")),
                                       (int(WIDTH / 8), int(HEIGHT / 8)))

class Asteroid:
    def __init__(self, rank, sw, sh, image):
        self.rank = rank

        self.bounds = 8

        if self.rank == 1:
            self.image = SMALL_ASTEROID
        elif self.rank == 2:
            self.image = MEDIUM_ASTEROID
        else:
            self.image = HUGE_ASTEROID

        self.w = self.image.get_width() - self.bounds
        self.h = self.image.get_height() - self.bounds

        self.x = round(random.choice([random.randrange(20, 130), random.randrange(sw - 150 - self.w, sw - 150)]))
        self.y = round(random.choice([random.randrange(20, 130), random.randrange(sh - 150 - self.h, sh - 150)]))

        if self.x < sw // 2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh // 2:
            self.ydir = 1
        else:
            self.ydir = -1

        self.xv = self.xdir * random.randrange(2, 3)
        self.yv = self.ydir * random.randrange(2, 3)

    def asteroid_hit_box(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def is_here(self, x, y):
        if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            return True
        else:
            return False

    def draw(self, window):
        # pygame.draw.rect(window, (155, 255, 0), [self.x, self.y, self.w, self.h])
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.xv
        self.y += self.yv

    def check_off_screen(self, sw, sh):
        if self.x < -self.w or self.x > sw or self.y > sh or self.y < -self.h:
            return True

    def check_location(self, sw, sh):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        if self.y > sh + 50:
            self.y = 0
        elif self.y < 9 - self.h:
            self.y = sh