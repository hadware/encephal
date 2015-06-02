__author__ = 'marechaux'

from numpy import *
from scipy.ndimage import *
from scipy.signal import *
from nodes.node import *
from enum import Enum


class FullConnexion(PipeNode):
    """ Basic connection type: all of the ouputs from the input node are connected to
    all the inputs of the output node.

    Attributes:
      matrix (numpy.darray): a matrix of the weights applied to the outputs from the intput node
    """

    def __init__(self, input_datasink, output_datasink):
        super().__init__(input_datasink, output_datasink)
        self.matrix = zeros((self.input_total_size, self.output_total_size))

    def randomize(self):
        """Sets up a random value for all the connections, i.e., randomizes the weight matrix"""
        self.matrix = 0.01*(random.random_sample((self.input_total_size, self.output_total_size)) - 0.5)
        #TODO: make parameters for the randomize

    def propagation(self, learning):
        """Propagates the input data from the input node to the next node, while """
        self.output_socket.prop_data[:] += dot((self.input_socket.prop_data).reshape(self.input_total_size), self.matrix).reshape(self.output_shape)

    def backpropagation(self):
        """Backpropagates the error gradient to the input node"""
        self.input_socket.backprop_data[:] += dot(self.matrix, (self.output_socket.backprop_data).reshape(self.output_total_size)).reshape(self.input_shape)

    def learn(self, alpha):
        """Applies the calculated error to the matrix"""
        self.matrix[:, :] -= alpha * dot(matrix((self.input_socket.prop_data).reshape(self.input_total_size)).transpose(), matrix((self.output_socket.backprop_data).reshape(self.output_total_size)))

class ConvolutionalConnexion(PipeNode):
    """
    Convolutional connexion, a kernel is convolved with the input_data

    Attributes:
    kernel (nparray): n dimensional kernel we desire to apply
    kernel_shape (list): shape of the kernel
    zero_padding (ZeroPadding): type of  zero padding we desire to apply for the convolution
    """

    def __init__(self, input_datasink, kernel_shape, zero_padding):
        self.kernel_shape = kernel_shape
        self.zero_padding = zero_padding
        self.kernel = zeros(self.kernel_shape)
        output_datasink = type(input_datasink)(self.compute_output_shape(input_datasink.shape_data))
        super().__init__(input_datasink, output_datasink)

    #Computing the output_shape knowing the input_shape, kernel_shape and zero_padding
    def compute_output_shape(self,input_shape):
        output_shape=[]
        #Filling the output_shape list
        for m , k in self.input_shape, self.kernel_shape:
            output_shape.append(m + self.zero_padding[0]*(k-1))
        return output_shape

    def randomize(self):
        """Sets up a random value for all the parameters of the kernel"""
        self.kernel = 0.01*(random.random_sample(self.kernel_shape) - 0.5)
        #TODO: make parameters for the randomize

    def propagation(self, learning):
        '''Propagates the input data with the convolution to the next node
        FFT is generally much faster than convolve for large arrays (n > ~500), but can be slower when only a few output values are needed
        or we could use: output_socket.prop_data[:] += convolve(self.input_socket.prop_data, self.kernel, mode=self.zero_padding)
        or with more options there is also:
        output_socket.prop_data[:] += convolve(self.input_socket.prop_data, self.kernel, mode='constant', cval=0.0)'''
        self.output_socket.prop_data[:] += fftconvolve(self.input_socket.prop_data, self.kernel, mode=self.zero_padding[1])

    def backpropagation(self):
        """Backpropagates the error gradient to the input node"""
        self.input_socket.backprop_data[:] += dot(self.matrix, (self.output_socket.backprop_data).reshape(self.output_total_size)).reshape(self.input_shape)

    def learn(self, alpha):
        #fftconvolve require the largest ndarray as the first parameter
        if self.zero_padding == ZeroPadding.full:
            self.kernel [:] += fftconvolve(self.output_socket.backprop_data,self.input_socket.prop_data, mode=self.zero_padding[1])
        else:
            self.kernel[:] += fftconvolve(self.input_socket.prop_data,self.output_socket.backprop_data, mode=self.zero_padding[1])

class PoolingConnexion(PipeNode):
    """
    Convolutional connexion, a kernel

    Attributes:

    """

class ZeroPadding(Enum):
    """ Enum type to caracterize of zero padding type as a tuple
    tuple[0] is a coefficient to find the output_shape knowing the input_shape and the kernel's size.
    tuple[1] is a string corresponding to the zero padding type """
    valid = (-1,'valid')
    same  = (0,'same')
    full  = (1,'full')