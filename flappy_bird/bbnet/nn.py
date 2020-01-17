import numpy as np
import scipy.special


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate=0.1):
        self.inodes = input_nodes
        self.hnodes = hidden_nodes
        self.onodes = output_nodes
        self.lr = learning_rate
        self.weights_ih = np.random.rand(hidden_nodes, input_nodes) - 0.5
        self.weights_ho = np.random.rand(output_nodes, hidden_nodes) - 0.5
        self.activate_function = lambda x: scipy.special.expit(x)

    def train(self, inputs, targets):
        # convert inputs list to 2d array
        inputs = np.array(inputs, ndmin=2).T
        targets = np.array(targets, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = np.dot(self.weights_ih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activate_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = np.dot(self.weights_ho, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activate_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = np.dot(self.weights_ho.T, output_errors)

        # update the weights for the links between the hidden and output layers
        self.weights_ho += self.lr * \
            np.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                   np.transpose(hidden_outputs))

        # update the weights for the links between the input and hidden layers
        self.weights_ih += self.lr * \
            np.dot((hidden_errors * hidden_outputs *
                    (1.0 - hidden_outputs)), np.transpose(inputs))

    def guess(self, inputs):
        inputs = np.array(inputs, ndmin=2).T
        hidden_inputs = np.dot(self.weights_ih, inputs)
        hidden_outputs = self.activate_function(hidden_inputs)
        final_inputs = np.dot(self.weights_ho, hidden_outputs)
        final_outputs = self.activate_function(final_inputs)
        return final_outputs

    def mutate(self, func):
        # Mutate each weights of the hidden and output layers
        for i in range(len(self.weights_ih)):
            for j in range(len(self.weights_ih[i])):
                self.weights_ih[i][j] = func(self.weights_ih[i][j])
        for i in range(len(self.weights_ho)):
            for j in range(len(self.weights_ho[i])):
                self.weights_ho[i][j] = func(self.weights_ho[i][j])

    @staticmethod
    def copy(nn: 'NeuralNetwork'):
        nn_cpy = NeuralNetwork(nn.inodes, nn.onodes, nn.hnodes)
        nn_cpy.weights_ho = np.copy(nn.weights_ho)
        nn_cpy.weights_ih = np.copy(nn.weights_ih)
        return nn_cpy
