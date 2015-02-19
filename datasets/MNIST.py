__author__ = 'marechaux'

import os
import struct
from numpy import *
from . import labeled_database

class MNIST(labeled_database.LabeledDatabase):

    def __init__(self, database):
        super().__init__()
        data, labels = self.read(database)

        self.input_size = 784
        self.nb_input = labels.size

        for i in range(0, labels.size):
            self.database.append((data[i].reshape((784))/255, labels[i]))

#TODO : make path more usable
    def read(self, dataset="training", path="./MNIST"):
        """
        Python function for importing the MNIST data set.  It returns an iterator
        of 2-tuples with the first element being the label and the second element
        being a numpy.uint8 2D array of pixel data for the given image.
        """

        if dataset is "training":
            fname_img = os.path.join(path, 'train-images.idx3-ubyte')
            fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
        elif dataset is "testing":
            fname_img = os.path.join(path, 't10k-images.idx3-ubyte')
            fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
        else:
            raise ValueError("dataset must be 'testing' or 'training'")

        # Load everything in some numpy arrays
        with open(fname_lbl, 'rb') as flbl:
            magic, num = struct.unpack(">II", flbl.read(8))
            lbl = fromfile(flbl, dtype=int8)

        with open(fname_img, 'rb') as fimg:
            magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
            img = fromfile(fimg, dtype=uint8).reshape(len(lbl), rows, cols)

        return img, lbl
