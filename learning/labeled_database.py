__author__ = 'marechaux'


class LearnLabeledDatabase:

    def __init__(self, network, database, encoder):
        self.network = network
        self.database = database
        self.encoder = encoder

    def online_learn(self, nb_iteration, alpha):
        for i in range(nb_iteration):
            data, label = self.database.random_element()
            self.network.input_layer.input_data_prop[:] = data
            self.network.propagation()
            self.network.output_layer.grad_error(self.encoder.encode(label))
            self.network.backpropagation()
            self.network.learn(alpha)

    def conv_bacth_learn(self, epsilon, alpha, print_result):
        error = epsilon + 1
        i=0
        while error > epsilon:
            i+=1
            error = 0
            for data, label in self.database.database:
                self.network.input_layer.input_data_prop[:] = data
                self.network.propagation()
                #print(self.network.output_layer.output_data_prop)
                error += self.network.output_layer.error(self.encoder.encode(label))
                self.network.output_layer.grad_error(self.encoder.encode(label))
                self.network.backpropagation()
                self.network.learn(alpha)
            if print_result and i%100==0:
                print(error)