__author__ = 'marechaux'

from subnet.subnet import *
from subnet.size import *
from nodes.layer import *
from nodes.full_connexion import *
from subnet.network import *
from datasets.logical_function import *
from execution.training.labeled_database import *
from execution.testing.labeled_database import *
from datasets.encoder.onehot import *
from nodes.math_function.math_function import *
from datasets.MNIST import *

s = Subnet()

input_size = Size([784])

hidden_size = Size([200])

output_size = Size([10])

output_layer = PerceptronLayer(output_size, Sigmoid)
output_layer.randomize()

hidden_layer = PerceptronLayer(hidden_size, Sigmoid)
hidden_layer.randomize()

connexion1 = FullConnexion(input_size, hidden_size)
connexion1.randomize()

connexion2 = FullConnexion(hidden_size, output_size)
connexion2.randomize()

i = s.add_input(input_size)
o = s.add_output(output_layer)
h = s.add_node(hidden_layer)
s.add_node(connexion1, i, h)
s.add_node(connexion2, h, o)

n = Network(s)

db = LogicalFunctionDatabase("xor")
learn_db = MNIST("training")
test_db = MNIST("testing")
encoder = Onehot(output_size)

learning = TrainLabeledDatabase(n, learn_db, encoder, QuadraticError.differential)
testing = TestLabeledDatabase(n, test_db, encoder)

learning.online_learn(10000, 1)

print(testing.test(True))
