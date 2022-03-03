from Game import Game
from NeuralNetwork import *
import random


class Population:
    def __init__(self, size):
        self.agents = []
        self.best_agent = None
        self.generation = 1
        self.best_fitness = 0
        self.size_of_population = size

        self.mating_pool = [Game()]

        for i in range(size):
            self.agents.append(Game(True, True))

    def play(self):
        number = 0
        for agent in self.agents:
            number += 1
            agent.show_display = True
            agent.play_game()
            print(f"Agent number: {number} died")
            self.calculate_fitness(agent)

    @staticmethod
    def calculate_fitness(agent):
        print(f"My score is {agent.score}")
        print(f"My lifetime is {agent.lifetime}")
        if agent.score == 0:
            agent.fitness = 1 + 6 * agent.lifetime
            agent.fitness = agent.fitness ** 2
            return
        if agent.lifetime < 1:
            agent.fitness = agent.score + 1
            agent.fitness = agent.fitness ** 2
            return

        agent.fitness = agent.score + 5 * agent.lifetime
        agent.fitness = agent.fitness ** 2
            #agent.fitness = agent.fitness ** 2
        print(f"My fitness is {agent.fitness}\n")


    def find_best_agent(self):
        print(f"\n")
        for agent in self.agents:
            if agent.fitness > self.best_fitness:
                self.best_fitness = agent.fitness
                self.best_agent = agent
        print(f"Best score: {self.best_agent.score}")

    def natural_selection(self):
        self.mating_pool.clear()

        # Calculate best fitness
        self.find_best_agent()

        # Best fitness can't be zero
        if self.best_fitness == 0:
            self.best_fitness = 1

        for agent in self.agents:
            fitness = agent.fitness / self.best_fitness
            n = int(100 * fitness)
            for i in range(n):
                self.mating_pool.append(agent)

    def generate(self):
        self.agents.clear()
        self.generation += 1
        self.agents.append(self.best_agent)

        # Half with new random character
        for i in range(int(self.size_of_population / 4) - 1):
            partner_a = random.choice(self.mating_pool)

            child = Game()
            child.crossover(partner_a)
            child.mutate()

            self.agents.append(child)

        # Half beetwen itself
        for i in range(int(self.size_of_population / 4)-1):
            partner_a = random.choice(self.mating_pool)
            partner_b = random.choice(self.mating_pool)

            partner_a.crossover(partner_b)
            partner_a.mutate()

            self.agents.append(partner_a)
        for i in range(int(self.size_of_population / 4)-1):
            partner_a = random.choice(self.mating_pool)
            partner_a.crossover(partner_a)
            partner_a.mutate()

            self.agents.append(partner_a)
        for i in range(self.size_of_population - len(self.agents)):
            partner_a = random.choice(self.mating_pool)

            self.agents.append(partner_a)

    def show_best(self):
        the_best = self.agents[self.agents.index(self.best_agent)]

        the_best.active_disp()
        the_best.play_game(self.generation)

        print(f"BEST AGENT SCORE: {self.best_agent.score}")
        print(f"Time: {self.best_agent.lifetime}[s]\n")

        print(f"NOW BEST SCORE: {the_best.score}")
        print(f"Time: {the_best.lifetime}[s]")
