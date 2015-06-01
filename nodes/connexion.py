__author__ = 'marechaux'

from numpy import *
from scipy.ndimage import *
from scipy.signal import *
from nodes.node import *
from execution import protobuf

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

class Convolutional(PipeNode):
    """
    Convolutional connexion, a kernel

    Attributes:
    kernel (nparray): n dimensional kernel we desire to apply
    kernel_shape (list): int's, representing shape of the kernel
    zero_padding (str): type of  zero padding we desire to apply for the convolution
    """

    def __init__(self, input_datasink, kernel_shape, zero_padding):
        self.kernel_shape = kernel_shape
        self.zero_padding = zero_padding
        self.kernel = zeros((self.input_total_size, self.output_total_size))
        output_datasink = type(input_datasink)(self.compute_output_shape(input_datasink.shape_data))
        super().__init__(input_datasink, output_datasink)
        #TODO : Use an enum instead of strings for the the zero_padding

    #Computing the output_shape knowing the input_shape, kernel_shape and zero_padding
    def compute_output_shape(self,input_shape):
        output_shape=[]
        #coef_zero_padding in {-1,0,1}
        coef_zero_padding = None
        if self.zero_padding == "valid":
            coef_zero_padding = -1
        elif self.zero_padding == "same":
            coef_zero_padding = 0
        elif self.zero_padding == "full":
            coef_zero_padding = 1
        #Filling the output_shape list
        for m , k in self.input_shape, self.kernel_shape:
            output_shape.append(m + coef_zero_padding*(k-1))
        return output_shape

    def randomize(self):
        """Sets up a random value for all the parameters of the kernel"""
        self.kernel = 0.01*(random.random_sample(self.kernel_shape) - 0.5)
        # TODO: make parameters for the randomization

    def propagation(self, learning):
        '''Propagates the input data with the convolution to the next node
        FFT is generally much faster than convolve for large arrays (n > ~500), but can be slower when only a few output values are needed
        or we could use: output_socket.prop_data[:] += convolve(self.input_socket.prop_data, self.kernel, mode=self.zero_padding)
        or with more options there is also:
        output_socket.prop_data[:] += convolve(self.input_socket.prop_data, self.kernel, mode='constant', cval=0.0)'''
        self.output_socket.prop_data[:] += fftconvolve(self.input_socket.prop_data, self.kernel, mode=self.zero_padding)

    def backpropagation(self):
        """Backpropagates the error gradient to the input node"""
        self.input_socket.backprop_data[:] += dot(self.matrix, (self.output_socket.backprop_data).reshape(self.output_total_size)).reshape(self.input_shape)

    def learn(self, alpha):
        pass

    def _set_protobuff_pipenode_data(self, pipenode_protobuf_message):
        pipenode_protobuf_message.node_type = protobuf.PipeNode.CONVOLUTIONAL_LAYER
        # TODO: use enum to render the  zero padding type
        pipenode_protobuf_message.data.zero_padding = protobuf.ConvolutionalLayerData.FULL
        pipenode_protobuf_message.data.kernel_shape.extend(self.kernel_shape)
