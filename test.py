__author__ = 'marechaux'


import database.logical_function
from database.MNIST import *
from layer.layer import *
from math_function.math_function import *
from connexion.full_connexion import *
from connexion.copy_connexion import *
from network.network import *
from learning.labeled_database import *
from testing.labeled_database import *
from encoder import *

db = database.logical_function.LogicalFunctionDatabase("and")

encoder = onehot.Onehot(10)

input_layer = InputLayer(784)

dropout_layer = DropoutLayer(200, 0.2)

hidden_layer = PerceptronLayer(200, Sigmoid)
hidden_layer.randomize()

output_layer = OutputLayer(10, Sigmoid, QuadraticError)
output_layer.randomize()

FullConnexion(input_layer, hidden_layer)

CopyConnexion(hidden_layer, dropout_layer)

FullConnexion(dropout_layer, output_layer)

network = Network(input_layer, output_layer)
network.verify()


learn_db = MNIST("training")
test_db = MNIST("testing")

learning = LearnLabeledDatabase(network, learn_db, encoder)
learning.online_learn(10000, 1)
#learning.online_learn(60000, 0.3)
#learning.online_learn(100000, 0.1)
#learning.online_learn(60000, 0.03)
#learning.conv_bacth_learn(1, 0.5, True)


testing = TestLabeledDatabase(network, test_db, encoder)
print(testing.test(True))


