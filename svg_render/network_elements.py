__author__ = 'hadware'

from enum import Enum

class ElementType(Enum):
    NODE = 1
    CONNEXION = 2
    SUBNET = 3


class Element:
    """fake representation of a network element"""

    def __init__(self, type, tag):
        self.connected_to = list()
        self.type = type
        self.tag = tag

    def add_connection(self, element):
        if isinstance(element, list):
            self.connected_to += element
        else:
            self.connected_to.append(element)