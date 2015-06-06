__author__ = 'marechaux'

from random import *
from datasink.datasink import *
from execution import protobuf

class LabeledDatabase:

    def __init__(self):
        self.database = []
        self.encoder = None
        self.input_datasink = None
        self.output_datasink = None
        self.nb_input = 0

    def random_element(self):
        return self.database[randint(0, len(self.database)-1)]

    def to_testing_protobuf_message(self):
        data_entry = protobuf.DataEntry()
        data_entry.type = protobuf.DataEntry.TEST
        self.input_datasink.to_protobuf_message(data_entry.testDataEntry.input_datatype)

    def to_learning_protobuf_message(self):
        data_entry = protobuf.DataEntry()
        data_entry.type = protobuf.DataEntry.TEST
        self.input_datasink.to_protobuf_message(data_entry.trainDataEntry.input_datatype)
        self.output_datasink.to_protobuf_message(data_entry.trainDataEntry.output_datatype)
