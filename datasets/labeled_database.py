__author__ = 'marechaux'

from random import *
from nodes.datasink import *


class LabeledDatabase:

    def __init__(self):
        self.database = []
        self.encoder = None
        self.datasync = None
        self.nb_input = 0

    def random_element(self):
        return self.database[randint(0, len(self.database)-1)]