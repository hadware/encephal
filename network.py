__author__ = 'marechaux'


from heapq import heappush, heappop


class Network:
    """ Wraps around the graph of a network, takes care of scheduling the propagation and backpropagation of
    input and error data throughout the graph.

    A Network needs an input layer and and output layer to be able (back)propagate data and thus work.
    Attributes:
      input_layer (Node): the input layer for the network.
      output_layer (Node): the ouput layer of the network
    """

    def __init__(self, input_layer, output_layer):
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.sorted_node = [[]]
        self.sorted_connexion = [[]]

    def verify(self):
        """Verifies that the network's structure conforms to the rules, and builds priority lists for the nodes and
        connections, used to parallelize calculations"""
        #TODO:check non recusive

        # this block runs through the whole graph of the network, to enumerate all the nodes it contains
        no_level_nodes = set()
        no_level_nodes.add(self.input_layer)

        #setting up a heap, "bootstraping" it with the input layer
        heap = []
        heappush(heap, self.input_layer)
        while heap: #while the heap's not empty, we pop an element (from the head the heap)
            current_node = heappop(heap)
            #for each connection linked to the "output pad" of the current_node,
            # - we add the connection's output node to the heap (i.e., the node connected to the output of the current node)
            # - we add the connextion to the "no_level_nodes" list
            for connexion in current_node.output_connexions:
                if connexion.output not in no_level_nodes:
                    no_level_nodes.add(connexion.output)
                    heappush(heap, connexion.output)


        # this block takes care of building the priority lists
        for node in no_level_nodes: # for each node, we set the level value to infinity
            node.level = float("inf")

        # bootstrapping the level system : the input layer has a zero priority level
        k = 0
        self.input_layer.level = k
        self.sorted_node[k].append(self.input_layer)
        no_level_nodes = list( no_level_nodes )
        no_level_nodes.remove(self.input_layer)

        # using the "no_level_node" list (a list of the network's nodes),
        # we build a level-by-level list of nodes which all can be "executed" in parallel during the propagation
        # and backpropagation
        while no_level_nodes:

            k += 1
            self.sorted_node.append([])
            self.sorted_connexion.append([])

            for node in no_level_nodes:
                candidate = True

                #building the list of nodes and connection for each level
                for connexion in node.input_connexions:
                    if connexion.input.level >= k:
                        candidate = False

                if candidate:
                    node.level = k
                    self.sorted_node[k].append(node)
                    self.sorted_connexion[k-1].append(connexion)
                    no_level_nodes.remove(node)

    def propagation(self):
        """"Using the priority list computed by the verify function, we ask each node and connection to compute
        and propagate the data, priority "layer" after priority "layer"."""
        for i in range(len(self.sorted_node)):
            for connexion in self.sorted_connexion[i]:
                connexion.propagation()

            for node in self.sorted_node[i + 1]:
                node.propagation()

    def backpropagation(self):
        """"Using the priority list computed by the verify function, we ask each node and connection to compute
        and backpropagate the error gradient, priority "layer" after priority "layer", all in reverse order."""
        for i in reversed(range(len(self.sorted_node))):
            for node in self.sorted_node[i - 1]:
                node.backpropagation()

            for connexion in self.sorted_connexion[i]:
                connexion.backpropagation()

    def learn(self, alpha):
        """Asks all the elements in the network to "apply" the learning deltas they computed"""
        for node_list in self.sorted_node:
            for node in node_list:
                node.learn(alpha)

        for connexion_list in self.sorted_connexion:
            for connexion in connexion_list:
                connexion.learn(alpha)