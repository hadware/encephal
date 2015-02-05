__author__ = 'marechaux'


class LabeledDatabase:

    def __init__(self):
        self.database = []
        self.encoder = None
        self.input_size = 0
        self.nb_input = 0