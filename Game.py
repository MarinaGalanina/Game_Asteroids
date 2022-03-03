import pygame
import numpy as np
# import keyboard
import random
import math
import os

from Ship import Ship
from Bullet import Bullet
from Asteroid import Asteroid
from NeuralNetwork import NeuralNet

WIDTH, HEIGHT = 720, 720

# IMPORT PICTURES
SPACECRAFT = pygame.transform.scale(pygame.image.load(os.path.join("PICS", "spacecraft.png")),
                                    (int(WIDTH / 15), int(HEIGHT / 15)))
BG = pygame.transform.scale(pygame.image.load(os.path.join("PICS", "space.png")), (WIDTH, HEIGHT))
SMALL_ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join("PICS", "asteroid1.png")),
                                        (int(WIDTH / 20), int(HEIGHT / 20)))
MEDIUM_ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join("PICS", "asteroid2.png")),
                                         (int(WIDTH / 11), int(HEIGHT / 11)))
HUGE_ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join("PICS", "asteroid3.png")),
                                       (int(WIDTH / 8), int(HEIGHT / 8)))


class Game:
    def __init__(self, show_dis=False, ai_play=True):

        # GENERATE RANDOM NUMBERS
        self.seed = int(1000 * random.random())
        random.seed(self.seed)
        np.random.seed(self.seed)

        # MECHANICAL GAME
        self.score = 0  # How many asteroid destroyed
        self.A_TIME = 800
        self.asteroids_timer = self.A_TIME
        self.lives = 1
        self.is_dead = False

        self.bullet_count = 5
        self.shot_rate = 50
        self.shot_tim = 0
        self.can_shot = True

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.asteroids = []
        self.bullets = []

        # SHOW DISPLAY
        self.show_display = show_dis
        self.WIN = None
        # if self.show_display:
        self.active_disp()

        # AI
        self.ai_play = ai_play
        self.brain = NeuralNet(9, 16, 4)  # Here will be NeuralNet
        self.vision = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 1]], dtype=float)  # Input layer for NeuralNet
        self.decision = []  # Output layer for NeuralNet
        self.replay = False  # Show game

        # Genetic algorithm
        self.fitness = 0

        self.lifetime = 0  # How long AI lived

        # Generate Ship
        self.ship = Ship(WIDTH / 2, HEIGHT / 2, SPACECRAFT)

        # Generate asteroids        | !!!IN FUTURE ADD SEED TO GENERATE ASTEROIDS!!! |
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))

    # DRAW PLAYER, ASTEROIDS, BULLETS
    def show_game(self):
        self.ship.draw(self.WIN)

        for bullet in self.bullets:
            bullet.draw(self.WIN)

        for asteroid in self.asteroids:
            asteroid.draw(self.WIN)

    def active_disp(self):
        pygame.font.init()
        self.main_font = pygame.font.SysFont("comicsans", 30)
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.show_display = True

    # UPDATE ALL POSITION
    def update_positions(self):
        for bullet in self.bullets:
            if not bullet.check_lifetime():
                bullet.move()
            else:
                self.bullets.pop(self.bullets.index(bullet))
                self.bullet_count += 1

        for asteroid in self.asteroids:
            asteroid.move()

    def check_location(self):
        self.ship.check_location(WIDTH, HEIGHT)

        for bullet in self.bullets:
            bullet.check_location(WIDTH, HEIGHT)

        for asteroid in self.asteroids:
            asteroid.check_location(WIDTH, HEIGHT)

    # CHECK ALL COLLISIONS
    def check_collisions(self):
        for asteroid in self.asteroids:

            # COLLISION WITH SHIP
            if asteroid.asteroid_hit_box().colliderect(self.ship.ship_hit_box()):
                # DESTROY ASTEROID
                # self.asteroids.pop(self.asteroids.index(asteroid))
                # self.score += 1
                self.lives -= 1

            # COLLISION WITH BULLET
            for bullet in self.bullets:
                if asteroid.asteroid_hit_box().colliderect(bullet.bullet_hit_box()):

                    # CREATE NEW ASTEROIDS
                    if asteroid.rank == 3:
                        na1 = Asteroid(2, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HUGE_ASTEROID])
                        na2 = Asteroid(2, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HUGE_ASTEROID])

                        na1.x = asteroid.x
                        na1.y = asteroid.y
                        na2.x = asteroid.x
                        na2.y = asteroid.y

                        self.asteroids.append(na1)
                        self.asteroids.append(na2)
                    elif asteroid.rank == 2:
                        na1 = Asteroid(1, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HUGE_ASTEROID])
                        na2 = Asteroid(1, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HUGE_ASTEROID])

                        na1.x = asteroid.x
                        na1.y = asteroid.y
                        na2.x = asteroid.x
                        na2.y = asteroid.y

                        self.asteroids.append(na1)
                        self.asteroids.append(na2)

                    self.asteroids.pop(self.asteroids.index(asteroid))
                    self.bullets.pop(self.bullets.index(bullet))
                    self.score += 1
                    self.bullet_count += 1

    def new_asteroid(self):
        self.asteroids_timer -= 1
        if self.asteroids_timer <= 0:
            ran = random.choice([1, 1, 1, 2, 3, 2])
            self.asteroids.append(Asteroid(ran, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HUGE_ASTEROID]))
            self.asteroids_timer = self.A_TIME

    def look_in_all_directions(self):
        for i in range(8):
            self.vision[0][i] = self.look_here(self.ship.angle + i * 45)

        if self.bullet_count > 0 and self.can_shot:
            self.vision[0][8] = 1
        else:
            self.vision[0][8] = 0

    def look_here(self, angle):
        distance = 1
        while distance <= 290:
            x_d = self.ship.x + distance * math.cos(math.radians(angle + 90))
            y_d = self.ship.y + distance * math.sin(math.radians(angle + 90))

            for asteroid in self.asteroids:
                if asteroid.is_here(x_d, y_d):
                    pygame.draw.line(self.WIN, (205, 100, 201), (self.ship.x, self.ship.y), (x_d, y_d), 1)
                    return 10 / distance

            distance += 1
            if y_d > HEIGHT + 50:
                y_d = -50
            elif y_d < -50:
                y_d = HEIGHT + 50

            if x_d > WIDTH + 50:
                x_d = -50
            elif x_d < -50:
                x_d = WIDTH + 50
        # pygame.draw.line(self.WIN, (255, 255, 255), (self.ship.x, self.ship.y), (x_d, y_d), 1)
        return 1

    def key_pressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.ship.turn_left()
        if keys[pygame.K_d]:
            self.ship.turn_right()
        if keys[pygame.K_w]:
            self.ship.move_forvard()

    def event_get(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(self.ship))
                if event.key == pygame.K_1:
                    self.lives = 1
                    self.is_dead = False
                if event.key == pygame.K_p:
                    self.is_dead = True

    def redraw_window(self, genration):
        self.WIN.blit(BG, (0, 0))
        livesText = self.main_font.render(f"Generation: {genration}", True, (255, 255, 255))
        self.WIN.blit(livesText, (10, 10))

        livesscore = self.main_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.WIN.blit(livesscore, (WIDTH - 200, 10))

        self.look_in_all_directions()
        self.show_game()

        pygame.display.update()

    def make_decision(self):
        # print(self.decision)
        if self.decision[0][0] > 0.7:
            self.ship.move_forvard()

        if self.decision[1][0] > 0.7:
            self.ship.turn_left()
        elif self.decision[2][0] > 0.7:
            self.ship.turn_right()

        if self.decision[3][0] > 0.7:
            if self.bullet_count >= 0 and self.can_shot == True:
                self.bullets.append(Bullet(self.ship))
                self.bullet_count -= 1
                self.can_shot = False

    def game_init(self):
        self.score = 0  # How many asteroid destroyed
        self.A_TIME = 1000
        self.asteroids_timer = self.A_TIME
        self.lives = 1
        self.is_dead = False

        self.bullet_count = 5
        self.shot_rate = 50
        self.shot_tim = 0
        self.can_shot = True

        self.asteroids = []
        self.bullets = []

        self.lifetime = 0  # How long AI lived

        # Generate Ship
        self.ship = Ship(WIDTH / 2, HEIGHT / 2, SPACECRAFT)

        # Generate asteroids        | !!!IN FUTURE ADD SEED TO GENERATE ASTEROIDS!!! |
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))
        self.asteroids.append(Asteroid(3, WIDTH, HEIGHT, [SMALL_ASTEROID, MEDIUM_ASTEROID, HEIGHT]))

    def play_game(self, generation=0):

        self.game_init()
        while not self.is_dead:

            self.clock.tick(self.FPS)

            if not self.can_shot:
                self.shot_rate -= 1
                if self.shot_rate <= 0:
                    self.can_shot = True
                    self.shot_rate = 50

            self.lifetime += 1

            if self.lives <= 0:
                self.is_dead = True

            self.update_positions()
            self.check_collisions()
            self.check_location()
            self.new_asteroid()
            self.look_in_all_directions()

            self.decision = self.brain.get_out(self.vision.T)

            self.make_decision()

            if self.show_display:
                self.redraw_window(generation)

                self.key_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.bullet_count >= 0 and self.can_shot:
                                self.bullets.append(Bullet(self.ship))
                                self.bullet_count -= 1
                                self.can_shot = False
                        if event.key == pygame.K_1:
                            self.lives = 1
                            self.is_dead = False
                        if event.key == pygame.K_p:
                            self.is_dead = True

        self.lifetime = self.lifetime / 60

    def crossover(self, partner):
        self.brain.crossover(partner.brain)

    def mutate(self):
        self.brain.mutate()
