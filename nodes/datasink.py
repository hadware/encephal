__author__ = 'hadware'
from .datatype import *
from numpy import zeros

class DataSink:
    """Holds data, and the datatype describing the data"""

    def __init__(self):
        self.type = None # a datatype
        self.data = None # the actual data

    def reinit_data(self):
        pass

    @property
    def shape(self):
        self.data.shape()

class Float2D(DataSink):

    def __init__(self, width, height):
        super().__init__()
        self.type = Vector(Vector(float, width), height)
        self.data = zeros((height, width))

    @property
    def height(self):
        return self.type.dim

    @property
    def width(self):
        return self.type.child_datatype.dim

    def reinit_data(self):
        self.data[:] = zeros((self.height, self.width))

class Float1D(DataSink):

    def __init__(self, length):
        super().__init__()
        self.type = Vector(float, length)
        self.data = zeros(length)

    @property
    def length(self):
        return self.type.dim

    def reinit_data(self):
        self.data[:] = zeros(self.length)
