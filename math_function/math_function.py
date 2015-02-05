__author__ = 'marechaux'


from numpy import *

#TODO : Add softmax...

class Sigmoid:

    @staticmethod
    def function(x):
        return 1/(1+exp(x))

    @staticmethod
    def differential(y):
        return y*(1-y)

class QuadraticError:

    @staticmethod
    def function(y, expected):
        return (y-expected)**2

    @staticmethod
    def differential(y, expected):
        return (y-expected)  #This is not exact but proportional to differential
