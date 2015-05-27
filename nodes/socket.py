__author__ = 'marechaux'


from numpy import *

class Socket:

    def __init__(self, datasink_class):
        self.input_nodes = [] # a list of OutputNodeSocket
        self.output_nodes = [] # a list of IntputNodeSocket

        #new instance of a datasink
        self.prob_datasink = datasink_class()
        self.backprob_datasink = datasink_class()

    def add_output_node(self, node):
        self.output_nodes.append(node)

    def add_input_node(self, node):
        self.input_nodes.append(node)

    @property
    def prop_data(self):
        return self.prob_datasink.data

    @property
    def backprop_data(self):
        return self.backprob_datasink.data
