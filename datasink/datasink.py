__author__ = 'hadware'
from numpy import zeros

from datasink.datatype import *


class DataSink:
    """
    Describe the data we are handling.
    Attributes:
        type (Datatype)
        shape_data (list):
        prop_data (nparray):
        backprop_data (nparray):
    """

    def __init__(self):
        self.type = None
        self.shape_data = None
        self.prop_data = None
        self.backprop_data = None

    def init_data(self):
        pass

    def reinit_data(self):
        pass

    #Compute the size of the equivalent flat 1D array
    @property
    def total_size(self):
        sum=1
        for elm in self.shape_data:
            sum *= elm
        return sum

class Float1D(DataSink):

    def __init__(self, shape):
        super().__init__()
        self.type = Vector(float, shape[0])
        self.shape_data=shape

    def init_data(self):
        self.prop_data = zeros(self.shape_data)
        self.backprop_data = zeros(self.shape_data)

    def reinit_data(self):
        self.prop_data[:] = zeros(self.shape_data)
        self.backprop_data[:] = zeros(self.shape_data)

class Float2D(DataSink):

    def __init__(self, shape):
        super().__init__()
        self.type = Vector(Vector(float, shape[0]), shape[1])
        self.shape_data=shape

    def init_data(self):
        self.prop_data = zeros(self.shape_data)
        self.backprop_data = zeros(self.shape_data)

    def reinit_data(self):
        self.prop_data[:] = zeros(self.shape_data)
        self.backprop_data[:] = zeros(self.shape_data)

