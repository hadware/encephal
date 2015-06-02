__author__ = 'lrx'

""" Define all the exception that are launch during the construction and are catched in our tests """

""" In construction Exception """

class InConstructionError(Exception):
    pass


""" After construction Exception """

class AfterConstructionError(Exception):
    pass

class EmptySubnetError(AfterConstructionError):
    pass

class NoNodeError(AfterConstructionError):
    pass

class NoInputError(AfterConstructionError):
    pass

class NoOutputError(AfterConstructionError):
    pass

class SubnetPresenceError(AfterConstructionError):
    pass

class NoInputSocketForEachNode(AfterConstructionError):
    pass

class NodeConnectedToItself(AfterConstructionError):
    pass

class NoConvexError(AfterConstructionError):
    pass
