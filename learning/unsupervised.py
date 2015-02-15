__author__ = 'marechaux'




class LearnUnsupervised:

    def __init__(self, network, database):
        self.network = network
        self.database = database

    def online_learn(self, nb_iteration, alpha):
        for i in range(nb_iteration):
            data, label = self.database.random_element()
            self.network.input_layer.input_data_prop[:] = data
            self.network.learn(alpha)
