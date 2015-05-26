__author__ = 'marechaux'

from subnet.subnet import *
from nodes.layer import *
from nodes.full_connexion import *
from subnet.network import *
from datasets.logical_function import *
from execution.training.labeled_database import *
from execution.testing.labeled_database import *
from datasets.encoder.onehot import *
from nodes.math_function.math_function import *
from datasets.MNIST import *

test_subnet = Subnet()

input_size = 784

hidden_size = 200

output_size = 10

output_layer = PerceptronLayer(output_size, Sigmoid)
output_layer.randomize()

hidden_layer = PerceptronLayer(hidden_size, Sigmoid)
hidden_layer.randomize()

connexion1 = FullConnexion(input_size, hidden_size)
connexion1.randomize()

connexion2 = FullConnexion(hidden_size, output_size)
connexion2.randomize()

input_socket = test_subnet.add_input(input_size)
output_socket = test_subnet.add_output(output_layer)
h = test_subnet.add_node(hidden_layer)
test_subnet.add_node(connexion1, input_socket, h)
test_subnet.add_node(connexion2, h, output_socket)

n = Network(test_subnet)

db = LogicalFunctionDatabase("xor")
learn_db = MNIST("training")
test_db = MNIST("testing")
encoder = Onehot(output_size)

learning = TrainLabeledDatabase(n, learn_db, encoder, QuadraticError.differential)
testing = TestLabeledDatabase(n, test_db, encoder)

learning.online_learn(10000, 1)

print(testing.test(True))
