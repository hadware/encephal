__author__ = 'hadware'

"""Downloader and managers for all types for dataset

Datasets are stored in ~/.encephal/datasets
"""

DATASETS_DIRECTORY = "~/.encephal/datasets"
MNIST_DOWNLOAD_LINKS = ["http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
                        "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
                        "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
                        "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"]

CIFAR10_DOWNLOAD_LINK = "http://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz"


class DatasetManager:
    def __init__(self, folder_name):
        pass

    def _check(self):
        """Checks if the dataset is already in the ~/.encephal/datasets/<datasetname> directory,
        and the validity using various methods (mostly checksum)"""
        pass

    def _check_dataset_folder(self):
        """Checks if ~/.encephal/datasets/<datasetname> is already here, if not, creates it"""
        pass


class MNISTManager(DatasetManager):
    pass


class CIFARManager(DatasetManager):
    pass
