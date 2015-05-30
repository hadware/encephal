__author__ = 'marechaux'

from random import *
from datasink.datasink import *

class LabeledDatabase:

    def __init__(self):
        self.database = []
        self.encoder = None
        self.input_datasink = None
        self.output_datasink = None
        self.nb_input = 0

    def random_element(self):
        return self.database[randint(0, len(self.database)-1)]