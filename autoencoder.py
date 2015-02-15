__author__ = 'marechaux'

import database.logical_function
from database.MNIST import *
from layer.layer import *
from math_function.math_function import *
from connexion.full_connexion import *
from connexion.copy_connexion import *
from connexion.reference_reversed_connexion import *
from network.network import *
from learning.labeled_database import *
from testing.labeled_database import *
from encoder import *

class Autoencoder:

    def __init__(self, input_size,  hidden_layer_size, output_size):
        input_layer = InputLayer(input_size)

        #dropout_layer = DropoutLayer(inphidden_layer_sizeut_size, 0.2)

        hidden_layer = PerceptronLayer(hidden_layer_size, Sigmoid)
        hidden_layer.randomize()

        output_layer = OutputLayer(output_size, Sigmoid, QuadraticError)
        output_layer.randomize()

        connexion = FullConnexion(input_layer, hidden_layer)

        #CopyConnexion(hidden_layer, dropout_layer)

        FullConnexion(hidden_layer, output_layer)

        self.network = Network(input_layer, output_layer)
        self.network.verify()

        output_layer_autoencoder = OutputLayer(input_size, Sigmoid, QuadraticError)
        output_layer_autoencoder.randomize()

        ReferenceReversedConnexion(hidden_layer, output_layer_autoencoder, connexion)

        self.autoencoder_network = AutoencoderNetwork(input_layer, output_layer_autoencoder)
        self.autoencoder_network.verify()


class AutoencoderNetwork(Network):

    def learn(self, alpha):
        self.propagation()
        self.output_layer.grad_error(self.input_layer.input_data_prop)
        self.backpropagation()
        super().learn(alpha)



learn_db = MNIST("training")
test_db = MNIST("testing")

autoencoder = Autoencoder(784, 100, 10)

encoder = onehot.Onehot(10)

learning = LearnLabeledDatabase(autoencoder.network, learn_db, encoder)

learning.online_learn(10000, 1)


testing = TestLabeledDatabase(autoencoder.network, test_db, encoder)
print(testing.test(True))


