__author__ = 'marechaux'


from . import encoder
from numpy import *

class Onehot(encoder.Encoder):

    def encode(self, label):
        result = zeros(self.size.total_size)
        result[label] = 1
        return result

    def decode(self, data):
        return data.argmax()
