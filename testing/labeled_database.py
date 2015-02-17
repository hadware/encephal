__author__ = 'marechaux'


class TestLabeledDatabase:

    def __init__(self, network, database, encoder):
        self.network = network
        self.database = database
        self.encoder = encoder

    def test(self, print_result):
        nb_ok = 0
        for data, label in self.database.database:
            self.network.input_layer.prop_data[:] = data
            self.network.propagation()
            result = self.encoder.decode(self.network.output_layer.prop_data)
            if print_result:
                print(label, " :", self.network.output_layer.prop_data)
            if result == label:
                nb_ok += 1
            self.network.init_buffer()
        return nb_ok / len(self.database.database)