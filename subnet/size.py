__author__ = 'lrx'

class Size:

    #TODO add the number of channel in the socket
    """
    Represents the shape of a mutlidimensional, multichannel data
    Socket will use it to represent complex data with 1D array.

    Attributes:
        dim (int): a channel's dimension
        dim_size (list):the list of the size of each dimension
        total_size (int):product of dim_size elements is precomputed.
    """

    def __init__(self, dim_size):
        self.dim=dim_size.__len__()
        self.dim_size=dim_size
        self.total_size=1
        for s in dim_size:
            self.total_size *=s
