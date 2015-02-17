__author__ = 'hadware'

from enum import Enum
from svg_render import grid_objects
from sys import maxsize

class Network:
    """fake representation of a network"""

    def __init__(self, input_node, output_node):
        self.input_node = input_node
        self.output_node = output_node


    def build_graph(self, filename):
        """Builds the graph for the network"""

        #gathering all the nodes the graph contains into a single list
        found_nodes = [self.input_node]
        heap = [self.input_node]
        while heap: #while the heap's not empty
            current_node = heap.pop(0)
            for node in current_node.connected_to:
                if node not in found_nodes:
                    found_nodes.append(node)
                    heap.append(node)

        #setting all nodes hierarchy to infinity
        for node in found_nodes:
            node.hierarchy = maxsize
        self.input_node.hierarchy = 0 #excepting, of course, the entry node

        remaining_nodes = found_nodes[:]
        #base the hierarchy with the input node
        current_level = 0
        self.hierarchised_nodes = list()
        self.hierarchised_nodes.append([self.input_node])
        remaining_nodes.remove(self.input_node)

        while remaining_nodes:
            current_level += 1
            self.hierarchised_nodes.append(list())

            for current_node in list(remaining_nodes):
                is_candidate = True

                for potential_predecessor in found_nodes:
                    if current_node in potential_predecessor.connected_to:
                        #current_node is preceded by potential_predecessor
                        if potential_predecessor.hierarchy >= current_level:
                            is_candidate = False

                if is_candidate:
                    current_node.hierarchy = current_level
                    self.hierarchised_nodes[current_level].append(current_node)
                    remaining_nodes.remove(current_node)

        # finding out the grid's dimension using the hierarchy

        grid = grid_objects.GraphGrid(self.hierarchised_nodes)










