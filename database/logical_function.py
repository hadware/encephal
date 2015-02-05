__author__ = 'marechaux'

from . import labeled_database

from numpy import *

class LogicalFunctionDatabase(labeled_database.LabeledDatabase):

    def __init__(self, operator):
        super().__init__()

        self.input_size = 2
        self.nb_input = 4

        if operator == "xor":
            table = self.xor_table()
        elif operator == "and":
            table = self.and_table()
        elif operator == "or":
            table = self.or_table()
        elif operator == "a":
            table = self.a_table()
        elif operator == "b":
            table = self.b_table()
        else:
            raise ValueError("operator must be 'xor', 'and', 'or', 'a' or 'b'")

        for i in range(4):
            data = [i//2, i%2]
            self.database.append((array(data), table[i]))

    def xor_table(self):
        return {0: 0, 1: 1, 2: 1, 3: 0}

    def and_table(self):
        return {0: 0, 1: 0, 2: 0, 3: 1}

    def or_table(self):
        return {0: 0, 1: 1, 2: 1, 3: 1}

    def a_table(self):
        return {0: 0, 1: 0, 2: 1, 3: 1}

    def b_table(self):
        return {0: 0, 1: 1, 2: 0, 3: 1}