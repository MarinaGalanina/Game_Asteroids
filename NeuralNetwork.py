import numpy as np
from random import random


def sigmoid_fun(x):
    return 1 / (1 + np.exp(-x))


class NeuralNet:
    def __init__(self, input, hidden, output):

        # SIZE OF MATRIXS LAYERS
        self.input = input
        self.hidden = hidden
        self.output = output

        # MAKE RANDOM OMEGA VALUES
        # PLUS ONE FOR BIAS
        self.w_in = np.array(2 * np.random.random((self.hidden, self.input + 1)) - 1)
        self.w_hidden = np.array(2 * np.random.random((self.hidden, self.hidden + 1)) - 1)
        self.w_output = np.array(2 * np.random.random((self.output, self.hidden + 1)) - 1)

    # print(f"in: \n {self.w_in}\n")
    # print(f"hid: \n {self.w_hidden}\n")
    # print(f"omega: \n {self.w_output}\n")

    def get_out(self, input_arr):
        # ADD ROW FOR BIAS
        input_arr = np.array(np.vstack([input_arr, 1]))

        sigmoid = np.vectorize(sigmoid_fun)

        # CALCULATE FIRST HIDDEN ARRAY
        first_layer_vector = np.matmul(self.w_in, input_arr)
        first_layer_vector = sigmoid(first_layer_vector)

        # ADD ROW BIAS
        first_layer_vector = np.array(np.vstack([first_layer_vector, 1]))
        # print(f"first layer vector: \n{first_layer_vector}")

        # CALCULATE SECOND HIDDEN ARRAY
        second_layer_vector = np.matmul(self.w_hidden, first_layer_vector)
        second_layer_vector = sigmoid(second_layer_vector)

        # ADD ROW BIAS
        second_layer_vector = np.array(np.vstack([second_layer_vector, 1]))
        #  print(f"second layer vector: \n{second_layer_vector}")

        # CALCULATE OUTPUT
        output = np.matmul(self.w_output, second_layer_vector)
        output = sigmoid(output)

        return output

    def mutate_change(self, omega):
        if random() < 0.15:
            omega = omega + np.random.random()
            if omega >= 1:
                omega = 0.9888
            elif omega <= -1:
                omega = -0.9888

            return omega
        else:
            return omega

    def crossover(self, partner):

        new = np.array(partner.w_in)

        ff = np.random.choice([2, 2, 3, 3, 3, 4, 4])
        dd = np.random.choice([1, 1, 1, 1, 2, 2, 2, 2, 3, 3])

        try:
            for i in range(int(self.w_in.shape[0] / dd)):
                if i % ff == 0:
                    self.w_in[i] = new[i]
        except ValueError:
            print("ups_in")

        new = np.array(partner.w_hidden)

        ff = np.random.choice([2, 2, 3, 3, 3, 4, 4])
        dd = np.random.choice([1, 1, 1, 1, 2, 2, 2, 2, 3, 3])
        try:
            for i in range(int(self.w_in.shape[0] / dd), self.w_hidden.shape[0]):
                if i % ff == 0:
                    self.w_hidden[i] = new[i]
        except ValueError:
            print("ups_hid")

        new = np.array(partner.w_output)

        ff = np.random.choice([2, 2, 3, 3, 3, 4, 4])
        dd = np.random.choice([1, 1, 1, 1, 2, 2, 2, 2, 3, 3])

        try:
            for i in range(int(self.w_output.shape[0] / dd)):
                if i % ff == 0:
                    self.w_output[i] = new[i]
        except ValueError:
            print("ups")

    def mutate(self):
        rd = np.vectorize(self.mutate_change)
        self.w_in = rd(self.w_in)
        self.w_hidden = rd(self.w_hidden)
        self.w_output = rd(self.w_output)
