import pygame


class Bullet:
    def __init__(self, ship):
        self.point = ship.head
        self.x = self.point[0]
        self.y = self.point[1]

        self.w = 3
        self.h = 3
        self.c = ship.cosine
        self.s = ship.sine
        self.xv = self.c * 5
        self.yv = self.s * 5

        self.lifetime = 150

    def check_lifetime(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            return True

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def bullet_hit_box(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def check_off_screen(self, sw, sh):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
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
