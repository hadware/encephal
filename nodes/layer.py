__author__ = 'marechaux'

from numpy import *
from nodes.node import *
from execution import protobuf

class PerceptronLayer(PipeNode):
    """
    A node representing a hidden layer of a perceptron network.

    Attributes:
      bias (numpy.ndarray): a ndarray of the layer's bias value for each unit (neuron)
      activation_function : the function the layer will use on the sum to compute the output value. Usually a sigmoid.
    """

    def __init__(self, datasink, activation_function):
        super().__init__(datasink, datasink)
        self.bias = zeros(self.input_shape)
        self.activation_function = activation_function

    def propagation(self, learning):
        self.output_socket.prop_data[:] += self.activation_function.function(self.input_socket.prop_data + self.bias)

    def backpropagation(self):
        """Computes the propagated error gradient for the hidden perceptron layer"""
        self.input_socket.backprop_data[:] += self.activation_function.differential_auxiliary(self.output_socket.prop_data) * self.output_socket.backprop_data

    def learn(self, alpha):
        """Modifies the bias array using the computed (and propagated) error gradient"""
        self.bias[:] -= alpha * self.input_socket.backprop_data

    def randomize(self):
        """Initialiazises all the biases for each internal neuron to a random value"""
        self.bias[:] = 0.01*(random.random_sample(self.input_shape)-0.5)

    def _set_protobuff_pipenode_data(self, pipenode_protobuf_message):
        pipenode_protobuf_message.node_type = protobuf.PipeNode.PERCEPTRON_LAYER
        pipenode_protobuf_message.data.perceptron_layer.activation_function = self.activation_function.to_protobuf_message()

class DropoutLayer(PipeNode):
    """
    A node representing a hidden layer of a Droupout.

    Attributes:
      filter (numpy.ndarray): a ndarray of
      p: the probability to keep
    """
    def __init__(self, datasink, p):
        super().__init__(datasink, datasink)
        self.filter = ones(self.input_shape)

        self.p = p

    def propagation(self, learning = True):
        if learning:
            self.filter[:] = random.binomial(1, self.p, self.input_shape)
            self.output_socket.prop_data[:] += self.input_socket.prop_data * self.filter
        else:
            self.output_socket.prop_data[:] += self.p * self.input_socket.prop_data

    def backpropagation(self):
        self.input_socket.backprop_data[:] += self.output_socket.backprop_data * self.filter

    def learn(self, alpha):
        pass

    def _set_protobuff_pipenode_data(self, pipenode_protobuf_message):
        pipenode_protobuf_message.node_type = protobuf.PipeNode.DROPOUT_LAYER
        pipenode_protobuf_message.data.dropout_layer.p = self.p
