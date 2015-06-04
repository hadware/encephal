__author__ = 'marechaux'


from .encoder import *
from numpy import *

class Onehot(Encoder):


    def encode(self, label):
        result = zeros(self.datasink.shape_data[0])
        result[label] = 1
        return result

    def decode(self, data):
        return data.argmax()
