__author__ = 'marechaux'


import database.logical_function
from layer.layer import *
from math_function.math_function import *
from connexion.full_connexion import *
from network import *
from learning.labeled_database import *
from testing.labeled_database import *
from encoder import *

db = database.logical_function.LogicalFunctionDatabase("and")

encoder = onehot.Onehot(2)

input_layer = InputLayer(2)

#hidden_layer = PerceptronLayer(4, Sigmoid)
#hidden_layer.randomize()

output_layer = OutputLayer(2, Sigmoid, QuadraticError)
output_layer.randomize()

#connexion1 = FullConnexion(input_layer, hidden_layer)
connexion1 = FullConnexion(input_layer, output_layer)
connexion1.randomize()

#connexion2 = FullConnexion(hidden_layer, output_layer)
#connexion2.randomize()

network = Network(input_layer, output_layer)
network.verify()

learning = LearnLabeledDatabase(network, db, encoder)
learning.online_learn(100000, 0.01)
#learning.conv_bacth_learn(1, 0.1, True)


testing = TestLabeledDatabase(network, db, encoder)
print(testing.test(True))


