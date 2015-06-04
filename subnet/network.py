__author__ = 'marechaux'

from execution import protobuf

class Network:

    def __init__(self, subnet):

        self.subnet = subnet.copy_reference()
        #Scheduling
        self.sorted_node = self.subnet.schedule()
        #Initialisation
        for socket in self.subnet.sockets:
            socket.socket_datasink.init_data()
        #Defining the input and output layer
        self.input_layer = self.subnet.input_node_sockets[0].connected_socket
        self.output_layer = self.subnet.output_node_sockets[0].connected_socket



    def propagation(self,learning = True):
        for node_list in self.sorted_node:
            for node in node_list:
                node.propagation(learning)

    def backpropagation(self):
        """"Using the priority list computed by the verify function, we ask each node and connection to compute
        and backpropagate the error gradient, priority "layer" after priority "layer", all in reverse order."""
        for node_list in reversed(self.sorted_node):
            for node in node_list:
                node.backpropagation()

    def learn(self, alpha):
        """Asks all the elements in the network to "apply" the learning deltas they computed"""
        for node_list in self.sorted_node:
            for node in node_list:
                node.learn(alpha)

    def randomize(self):
        self.subnet.randomize()

    def init_buffer(self):
        for socket in self.subnet.sockets:
            socket.socket_datasink.reinit_data()

    def to_protobuf_message(self):
        """Uses the scheduled nodes and sockets to build the protobuf graph sent to CUDA"""
        scheduled_graph_msg = protobuf.Graph()

        # first we add the sockets to the graph, giving each socket an index
        for i, socket in enumerate(self.subnet.sockets):
            socket.index = i
            scheduled_graph_msg.sockets.extend([socket.to_protobuf_message(i)])

        # then we add the scheduled nodes, layer by layer, and add the connections in the mean time
        i = 0
        for scheduled_layer in self.sorted_node:
            layer_msg = scheduled_graph_msg.node_layers.add()

            for node in scheduled_layer:
                node.index = i

                # adding the node to scheduled layer
                layer_msg.nodes.extend([node.to_protobuf_message(i)])

                # adding the two connections from this nodes to the connection list
                # input_connection, output_connection = protobuf.Connection(), protobuf.Connection()
                # input_connection.node_index = i
                # input_connection.socket_index = node.input_socket.index
                # output_connection.node_index = i
                # output_connection.socket_index = node.output_socket.index
                # scheduled_graph_msg.connections.extend([input_connection, output_connection])

                i += 1

        return scheduled_graph_msg
