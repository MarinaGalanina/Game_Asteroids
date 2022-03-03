import pygame
import math


class Ship:
    def __init__(self, x, y, image):
        self.ship_image = image

        self.bound = 15

        self.x = x
        self.y = y
        self.w = self.ship_image.get_width() - self.bound
        self.h = self.ship_image.get_height() - self.bound

        self.angle = 0
        self.angle_rate = 8
        self.rotatedSurf = pygame.transform.rotate(self.ship_image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)
        self.hit_box = pygame.Rect(self.x - self.w//2, self.y - self.h//2, self.w, self.h)

    def draw(self, window):
        # pygame.draw.rect(window, (255, 0, 255), self.hit_box)
        # pygame.draw.circle(window,(255,0,255),(self.x, self.y), 290)
        window.blit(self.rotatedSurf, self.rotatedRect)


    def ship_hit_box(self):
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)

    def turn_left(self):
        self.angle += self.angle_rate
        self.rotatedSurf = pygame.transform.rotate(self.ship_image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def turn_right(self):
        self.angle -= self.angle_rate
        self.rotatedSurf = pygame.transform.rotate(self.ship_image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def move_forvard(self):
        self.x += self.cosine * 3
        self.y -= self.sine * 3
        self.rotatedSurf = pygame.transform.rotate(self.ship_image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def check_location(self, sw, sh):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        if self.y > sh + 50:
            self.y = 0
        elif self.y < 9 - self.h:
            self.y = sh


