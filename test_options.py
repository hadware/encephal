__author__ = 'lrx'

from nodes.layer import *
from nodes.full_connexion import *
from nodes.math_function.math_function import *
from execution.training.labeled_database import *
from execution.testing.labeled_database import *
from nodes.datasink import *

"""
Class to choose how to fill a subnet with a given input_datasink and output_datasink
Make it possible to test easily different and new implementations
"""
class FillSubnet:

    @staticmethod
    def MLP(subnet,input_datasink,output_datasink):

        #Define the datasink
        hidden_datasink = Float1D(200)

        #Create the pipe nodes
        output_layer = PerceptronLayer(output_datasink, Sigmoid)
        hidden_layer = PerceptronLayer(hidden_datasink, Sigmoid)
        connexion1 = FullConnexion(input_datasink, hidden_datasink)
        connexion2 = FullConnexion(hidden_datasink, output_datasink)

        #Connect the pipe nodes
        subnet.connect_Pipe_nodes(connexion1,hidden_layer)
        subnet.connect_Pipe_nodes(hidden_layer,connexion2)
        subnet.connect_Pipe_nodes(connexion2,output_layer)

        #Create the input and output
        subnet.create_Pipe_input(connexion1)
        subnet.create_Pipe_output(output_layer)

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
            print('value' + str(i) + ':' + str(res))
            m += res
        print("The average score value is:")
        print(m/nb_values)
