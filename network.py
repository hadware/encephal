__author__ = 'marechaux'


from heapq import heappush, heappop


class Network:

    def __init__(self, input_layer, output_layer):
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.sorted_node = [[]]
        self.sorted_connexion = [[]]

    def verify(self):
        #TODO:check non recusive

        #Fill the set of node
        no_level_nodes = set()
        no_level_nodes.add(self.input_layer)
        heap = []
        heappush(heap, self.input_layer)
        while heap:
            element = heappop(heap)
            for connexion in element.output_connexion:
                if connexion.output not in no_level_nodes:
                    no_level_nodes.add(connexion.output)
                    heappush(heap, connexion.output)

        #fill the data structures
        for node in no_level_nodes:
            node.level = float("inf")
        k = 0
        self.input_layer.level = k
        self.sorted_node[k].append(self.input_layer)
        no_level_nodes = list( no_level_nodes )
        no_level_nodes.remove(self.input_layer)
        while no_level_nodes:
            k += 1
            self.sorted_node.append([])
            self.sorted_connexion.append([])
            for node in no_level_nodes:
                candidate  = True
                for connexion in node.input_connexion:
                    if connexion.input.level>=k:
                        candidate = False
                if candidate:
                    node.level = k
                    self.sorted_node[k].append(node)
                    self.sorted_connexion[k-1].append(connexion)
                    no_level_nodes.remove(node)

    def propagation(self):
        for i in range(1, len(self.sorted_node)):
            for connexion in self.sorted_connexion[i-1]:
                connexion.propagation()

            for node in self.sorted_node[i]:
                node.propagation()

    def backpropagation(self):
        for i in reversed(range(1, len(self.sorted_node))):
            for node in self.sorted_node[i]:
                if i==len(self.sorted_node)-1:
                    node.backpropagation()
                else:
                    node.backpropagation()

            for connexion in self.sorted_connexion[i-1]:
                connexion.backpropagation()

    def learn(self, alpha):
        for node_list in self.sorted_node:
            for node in node_list:
                node.learn(alpha)

        for connexion_list in self.sorted_connexion:
            for connexion in connexion_list:
                connexion.learn(alpha)