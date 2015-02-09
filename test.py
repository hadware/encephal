__author__ = 'marechaux'


import database.logical_function
from database.MNIST import *
from layer.layer import *
from math_function.math_function import *
from connexion.full_connexion import *
from network import *
from learning.labeled_database import *
from testing.labeled_database import *
from encoder import *

db = database.logical_function.LogicalFunctionDatabase("xor")

encoder = onehot.Onehot(10)

input_layer = InputLayer(784)

hidden_layer = PerceptronLayer(200, Sigmoid)
hidden_layer.randomize()

output_layer = OutputLayer(10, Sigmoid, QuadraticError)
output_layer.randomize()

connexion1 = FullConnexion(input_layer, hidden_layer)
#connexion1 = FullConnexion(input_layer, output_layer)
connexion1.randomize()

connexion2 = FullConnexion(hidden_layer, output_layer)
connexion2.randomize()

network = Network(input_layer, output_layer)
network.verify()


learn_db = MNIST("training")
test_db = MNIST("testing")

learning = LearnLabeledDatabase(network, learn_db, encoder)
learning.online_learn(600000, 0.005)
#learning.conv_bacth_learn(1, 0.5, True)


testing = TestLabeledDatabase(network, test_db, encoder)
print(testing.test(True))


