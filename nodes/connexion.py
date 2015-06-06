__author__ = 'marechaux'

from numpy import *
from scipy.ndimage import *
from scipy.signal import *
from nodes.node import *
from enum import Enum
from execution import protobuf
from nodes.math_function.pooling_function import *


class FullConnexion(PipeNode):
    """ Basic connection type: all of the ouputs from the input node are connected to
    all the inputs of the output node.

    Attributes:
      matrix (numpy.darray): a matrix of the weights applied to the outputs from the intput node
    """

    def __init__(self, input_datasink, output_datasink):
        super().__init__(input_datasink, output_datasink)
        self.matrix = None

    def init_data(self):
        self.matrix = zeros((self.input_total_size, self.output_total_size))

    def randomize(self):
        """Sets up a random value for all the connections, i.e., randomizes the weight matrix"""
        self.matrix = 0.01*(random.random_sample((self.input_total_size, self.output_total_size)) - 0.5)
        #TODO: make parameters for the randomize

    def propagation(self, learning):
        """Propagates the input data from the input node to the next socket """
        self.output_socket.prop_data[:] += dot((self.input_socket.prop_data).reshape(self.input_total_size), self.matrix).reshape(self.output_shape)

    def backpropagation(self):
        """Backpropagates the error gradient to the input socket"""
        self.input_socket.backprop_data[:] += dot(self.matrix, (self.output_socket.backprop_data).reshape(self.output_total_size)).reshape(self.input_shape)

    def learn(self, alpha):
        """Applies the calculated error to the matrix"""
        self.matrix[:, :] -= alpha * dot(matrix((self.input_socket.prop_data).reshape(self.input_total_size)).transpose(), matrix((self.output_socket.backprop_data).reshape(self.output_total_size)))

    def _set_protobuff_pipenode_data(self, pipenode_protobuf_message):
        pipenode_protobuf_message.node_type = protobuf.PipeNode.FULL_CONNEXION


class ConvolutionalConnexion(PipeNode):
    """
    Convolutional connexion, a kernel is convolved with the input_data

    Attributes:
    kernel (nparray): n dimensional kernel we desire to apply
    kernel_shape (list): int's, representing shape of the kernel
    zero_padding (ZeroPadding): type of  zero padding we desire to apply for the convolution
    """

    def __init__(self, input_datasink, kernel_shape, zero_padding):
        self.check_shape(input_datasink, kernel_shape)

        self.kernel_shape = kernel_shape
        self.zero_padding = zero_padding
        self.kernel = None
        output_datasink = type(input_datasink)(self.compute_output_shape(input_datasink.shape_data))
        super().__init__(input_datasink, output_datasink)

    def init_data(self):
        self.kernel = zeros(self.kernel_shape)

    @property
    def kernel_flipped(self):
        return fliplr(self.kernel)


    #Computing the output_shape knowing the input_shape, kernel_shape and zero_padding
    def compute_output_shape(self,input_shape):
        output_shape=[]
        #Filling the output_shape list
        for m , k in zip(input_shape, self.kernel_shape):
            output_shape.append(m + self.zero_padding.value[0]*(k-1))
        return output_shape

    def randomize(self):
        """Sets up a random value for all the parameters of the kernel"""
        self.kernel = 0.01*(random.random_sample(self.kernel_shape) - 0.5)
        # TODO: make parameters for the randomization

    '''FFT is generally much faster than convolve for large arrays (n > ~500), but can be slower when only a few output values are needed
    or we could use: output_socket.prop_data[:] += convolve(self.input_socket.prop_data, self.kernel, mode=self.zero_padding)
    or with more options there is also:output_socket.prop_data[:] += convolve(self.input_socket.prop_data, self.kernel, mode='constant', cval=0.0)
    WARNING: fftconvolve require the largest ndarray as the first parameter '''

    def propagation(self, learning):
        '''Propagates the input data with the convolution to the next node '''
        self.output_socket.prop_data[:] += fftconvolve(self.input_socket.prop_data, self.kernel, mode=self.zero_padding.value[1])

    def backpropagation(self):
        """Backpropagates the error gradient to the input node"""
        self.input_socket.backprop_data[:] += fftconvolve(self.output_socket.backprop_data, self.kernel_flipped, mode=self.zero_padding.value[2])

    #fliprl permet de flipper un np array
    def learn(self, alpha):
        self.kernel[:] += fftconvolve(self.input_socket.prop_data, self.output_socket.backprop_data, mode=self.zero_padding.value[1])

    def _set_protobuff_pipenode_data(self, pipenode_protobuf_message):
        pipenode_protobuf_message.node_type = protobuf.PipeNode.CONVOLUTIONAL_LAYER
        pipenode_protobuf_message.data.zero_padding = protobuf.ConvolutionalLayerData.FULL
        pipenode_protobuf_message.data.kernel_shape.extend(self.kernel_shape)

class ZeroPadding(Enum):
    """ Enum type to caracterize of zero padding type as a tuple
    tuple[0] is a coefficient to find the output_shape knowing the input_shape and the kernel's size.
    tuple[1] is a string corresponding to the zero padding type
    tuple[2] is a string corresponding to the 'opposite' zero_padding type"""
    VALID = (-1,'valid','full')
    SAME  = (0,'same','same')
    FULL  = (1,'full','valid')

class PoolingConnexion(PipeNode):
    """
    Pooling Connexion that intervene in a convolutional layer. This a Sub Sampling Layer

    Attributes:
    pooling_function : the function we will use to pool
    pooling_shape :
    stride_shape :
    """
    def __init__(self, input_datasink, pooling_function, pooling_shape, stride_shape):
        self.check_shape(input_datasink, pooling_shape)
        self.check_shape(input_datasink, stride_shape)

        self.pooling_function = pooling_function
        self.pooling_shape = pooling_shape
        self.stride_shape = stride_shape
        output_datasink = type(input_datasink)(self.compute_output_shape(input_datasink.shape_data))
        super().__init__(input_datasink, output_datasink)


    #Computing the output_shape knowing the input_shape, pooling_shape and stride_shape
    def compute_output_shape(self,input_shape):
        output_shape = []
        #Filling the output_shape list
        for i in range(input_shape.__len__()):
            #The pooling can be not on the entire input depending on the parameters, to check
            output_shape.append(((input_shape[i]-self.pooling_shape[i])//self.stride_shape[i])+1)
        return output_shape

    def propagation(self, learning):
        self.output_socket.prop_data[:] += self.pooling_function.pool(self.input_socket.prop_data)

    def backpropagation(self):
        self.input_socket.backprop_data[:] += self.pooling_function.pool_back(self.output_socket.backprop_data)

    def learn(self, alpha):
        pass







