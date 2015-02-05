__author__ = 'marechaux'


import database.logical_function
from layer.layer import *
from math_function.math_function import *
from connexion.full_connexion import *
from network import *

from encoder import *

db = database.logical_function.LogicalFunctionDatabase("and")

encoder = onehot.Onehot(2)

input_layer = InputLayer(2)

hidden_layer = PerceptronLayer(3, Sigmoid)

output_layer = OutputLayer(2, Sigmoid, QuadraticError)

connexion1 = FullConnexion(input_layer, hidden_layer)
connexion1.randomize()

connexion2 = FullConnexion(hidden_layer, output_layer)
connexion2.randomize()

network = Network(input_layer, output_layer)
print(connexion2.input)
network.verify()

print(network.sorted_node)
print(network.sorted_connexion)

data, label = db.database[1]

input_layer.input_data_prop[:] = data
print(input_layer.output_data_prop)
network.propagation()

print(output_layer.output_data_prop)

output_layer.error(encoder.encode(label))

network.backpropagation()
print(encoder.encode(label))
print(hidden_layer.input_data_prop)


