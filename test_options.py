__author__ = 'lrx'

from subnet.socket_size import *
from nodes.layer import *
from nodes.full_connexion import *
from nodes.math_function.math_function import *
from execution.training.labeled_database import *
from execution.testing.labeled_database import *

"""
Class to choose how to fill a subnet with a given input_size and output size
Make it possible to test easily different and new implementations
"""
class FillSubnet:

    @staticmethod
    def MLP(subnet,input_size,output_size):

        hidden_size = SocketSize([200])

        output_layer = PerceptronLayer(output_size, Sigmoid)

        hidden_layer = PerceptronLayer(hidden_size, Sigmoid)

        connexion1 = FullConnexion(input_size, hidden_size)

        connexion2 = FullConnexion(hidden_size, output_size)

        i = subnet.add_input(input_size)
        o = subnet.add_output(output_layer)
        h = subnet.add_node(hidden_layer)
        subnet.add_node(connexion1, i, h)
        subnet.add_node(connexion2, h, o)

"""
Class to calculate statistics on the performance of a network.
"""
class Statistic:

    def __init__(self,learn_db,test_db,encoder):
        self.learn_db=learn_db
        self.test_db=test_db
        self.encoder=encoder


    def test(self,n):
        n.randomize()
        learning = TrainLabeledDatabase(n, self.learn_db, self.encoder, QuadraticError.differential)
        testing = TestLabeledDatabase(n, self.test_db, self.encoder)
        learning.online_learn(10000, 1)
        res=testing.test(False)
        return res


    def mean(self,n,nb_values):
        m=0
        for i in range(nb_values):
            res = self.test(n)
            print('value' + str(i) + ':')
            print(res)
            m += res
        print("The average score value is:")
        print(m/nb_values)
