__author__ = 'marechaux'


class Connexion:
    """ This represents a connection between two Node objects.

    It has a unique input node, and a unique output node.
    In most subclasses, a connection stores the weight matrix to
    the output node as well.


    Attributes:
      input (Node): reference to the input node
      output (Node): reference to the output node
      input_size (int): size of the input node's array
      output_size (int): size of the output node's array
    """

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
