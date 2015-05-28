__author__ = 'hadware'

"""Describes the data types sent and received by sockets and nodes"""

class DataTypeError(Exception):
    pass

class DataType:

    def matches(self, data_structure):
        """Returns true if the datatypes from the other datastructure match recursively"""
        pass

class Vector(DataType):

    def __init__(self, child_datatype, dimension):
        self.dim = dimension
        self.child_datatype = child_datatype

    def matches(self, data_structure):

        #first, checking if the two data_structure really is a vector
        if isinstance(data_structure, Vector):
            if type(self.child_datatype) == type(data_structure.child_datatype) and self.dim == data_structure.dim:
                if self.child_datatype in (float, int, bool):
                    #its a "leaf" type, no need to recurse anymore
                    return True
                else:
                    #we've got to recursively keep on checking the type
                    return self.child_datatype.matches(data_structure.child_datatype)
            else:
                return False
        else:
            return False


class TimeSeries(DataType):

    def __init__(self, child_datatype):
        pass

    def matches(self, data_structure):
        pass
        #TODO : overload this one



if __name__ == "__main__":
    grid_size = 100
    grid = Vector(Vector(float, 100), 100)