__author__ = 'hadware'
from .datatype import *
from numpy import zeros

class DataSink:
    """Holds data, and the datatype describing the data"""

    def __init__(self):
        self.type = None # a datatype
        self.shape_data = None #the shape of the data
        self.data = None # the actual data

    def reinit_data(self):
        pass

    def total_size(self):
        sum=1
        for elm in self.shape_data:
            sum *= elm
        return sum

class Float1D(DataSink):

    def __init__(self, length):
        super().__init__()
        self.type = Vector(float, length)
        self.shape_data=[length]
        self.data = zeros(self.shape_data)

    def reinit_data(self):
        self.data[:] = zeros(self.shape_data)

class Float2D(DataSink):

    def __init__(self, width, height):
        super().__init__()
        self.type = Vector(Vector(float, width), height)
        self.shape_data=[height, width]
        self.data = zeros(self.shape_data)

    def reinit_data(self):
        self.data[:] = zeros(self.shape_data)


