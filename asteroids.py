from Game import Game
import numpy as np
from NeuralNetwork import NeuralNet
from Population import *


pop = Population(50)
i = 1
while True:
    print(f"\n \nGeneration: {i}")
    pop.play()
    pop.find_best_agent()

    pop.natural_selection()
    pop.generate()
    pop.best_fitness = 0
    i += 1

