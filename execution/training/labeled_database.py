__author__ = 'marechaux'

from gi.repository import GLib

class TrainLabeledDatabase:

    def __init__(self, network, database, encoder, error_function):
        self.network = network
        self.database = database
        self.encoder = encoder
        self.error_function = error_function

    def online_learn(self, nb_iteration, alpha, update_progress=None):
        """Does the online learning, if progress_callback is set, this function
        is called everystep to update on the progress"""
        for i in range(nb_iteration):
            if update_progress is not None:
                GLib.idle_add(update_progress, (i + 1) / nb_iteration)
            data, label = self.database.random_element()
            self.network.input_layer.prop_data[:] = data
            self.network.propagation()
            self.network.output_layer.backprop_data[:] = self.error_function(self.network.output_layer.prop_data, self.encoder.encode(label))
            self.network.backpropagation()
            self.network.learn(alpha)
            self.network.init_buffer()

    def conv_batch_learn(self, epsilon, alpha, print_result, progress_callback=None):
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