__author__ = 'marechaux'

from subnet.subnet import *
from layer.layer import *
from connexion.full_connexion import *
from subnet.network import *
from math_function.math_function import *
from numpy import *
from database.logical_function import *
from learning.labeled_database import *
from testing.labeled_database import *
from encoder.onehot import *
from math_function.math_function import *
from database.MNIST import *

s = Subnet()

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

learning = LearnLabeledDatabase(n, learn_db, encoder, QuadraticError.differential)
testing = TestLabeledDatabase(n, test_db, encoder)

learning.online_learn(60000, 1)
learning.online_learn(60000, 0.5)
learning.online_learn(60000, 0.2)
print(testing.test(True))
