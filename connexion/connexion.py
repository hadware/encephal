__author__ = 'marechaux'


class Connexion:

    def __init__(self, input_node, output_node):
        self.input = input_node
        self.output = output_node
        self.input_size = input_node.input_size
        self.output_size = output_node.output_size
        self.output_data = None
        self.input_data = None
        input_node.add_output_connexion(self)
        output_node.add_input_connexion(self)

    #TODO : exeption on get_input_value and get_output_value and store size...
