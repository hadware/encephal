__author__ = 'marechaux'

from datasink.socket import *
from nodes.node import *

class Subnet(Node):
    """
    Represent a subnet which is a a space of storage with multiple input_node_sockets and output_node_sockets.

    Attributes:
    nodes (list node): Set of nodes present in the Subnet
    sockets (list sockets): Set of sockets present in the Socket
    """

    def __init__(self):
        super().__init__()
        self.nodes = set()
        self.sockets = set()

    def create_input(self,input_node):
        #Add nodes
        self.nodes.add(input_node)
        for input_node_socket in input_node.input_node_sockets:
            self.create_node_socket_input(input_node_socket)

    def create_output(self,output_node):
        #Add nodes
        self.nodes.add(output_node)
        for output_node_socket in output_node.output_node_sockets:
            self.create_node_socket_output(output_node_socket)

    def connect_nodes(self,left_node,right_node):
        #Add nodes
        self.nodes.add(left_node)
        self.nodes.add(right_node)
        #Connect the node sockets
        for i in range(len(left_node.output_node_sockets)):
            self.connect_node_sockets(left_node.output_node_sockets[i],right_node.input_node_sockets[i])
        #TODO: Add the way nodes can connect between themselves
        #TODO: CLEAN: an iterator is preferable to a simple index


    """ Functions on node_socket """

    def create_node_socket_input(self,input_node_socket):
        #Creation of the socket
        if input_node_socket.connected_socket == None:
            socket = Socket(input_node_socket.datasink)
            self.sockets.add(socket)
            #Linking after check
            input_node_socket.connect_socket(socket)
        #Add one input_node_socket for the subnet
        self.input_node_sockets.append(input_node_socket)

    def create_node_socket_output(self,output_node_socket):
        #Creation of the socket and connexion with the node_socket
        if output_node_socket.connected_socket == None:
            socket=Socket(output_node_socket.datasink)
            self.sockets.add(socket)
            #Linking after check
            output_node_socket.connect_socket(socket)
        #Add one output_node_socket for the subnet
        self.output_node_sockets.append(output_node_socket)

    def connect_node_sockets(self,output_node_socket,input_node_socket):
        if output_node_socket.connected_socket == None and input_node_socket.connected_socket == None:
            #Creation of a socket
            socket=Socket(output_node_socket.datasink)
            self.sockets.add(socket)
            #Linking after check
            output_node_socket.connect_socket(socket)
            input_node_socket.connect_socket(socket)

        elif output_node_socket.connected_socket == None and input_node_socket.connected_socket != None:
            output_node_socket.connect_socket(input_node_socket.connected_socket)

        elif output_node_socket.connected_socket != None  and input_node_socket.connected_socket == None:
            input_node_socket.connect_socket(output_node_socket.connected_socket)

        else:#they already have a socket between them, we have to merge
            print("merge")
            pass










    #Un type de copie , il va  y en avoir d'autres
    def copy(self, input_translations = None, output_translations = None):
        clone = Subnet()

        socket_translator = {}

        if input_translations is not None:
            for i, input_socket in enumerate(input_translations):
                socket_translator[self.input_node_sockets[i]] = input_socket
        else:
            for input_socket in self.input_node_sockets:
                new_input_socket = Socket(input_socket.size)
                socket_translator[input_socket] = new_input_socket
                clone.sockets.add(new_input_socket)
                clone.input_node_sockets.append(new_input_socket)

        if output_translations is not None:
            for i, output_socket in enumerate(output_translations):
                socket_translator[self.output_node_sockets[i]] = output_socket
        else:
            for output_socket in self.output_node_sockets:
                new_output_socket = Socket(output_socket.size)
                socket_translator[output_socket] = new_output_socket
                clone.sockets.add(new_output_socket)
                clone.output_node_sockets.append(new_output_socket)


        for socket in self.sockets:
            if socket not in socket_translator:
                new_socket = Socket(socket.size)
                socket_translator[socket] = new_socket
                clone.sockets.add(new_socket)

        for node in self.nodes:
            input_socket = socket_translator[node.input_socket]
            output_socket = socket_translator[node.output_socket]
            new_node = GraphNode(node.node, input_socket, output_socket)
            input_socket.output_nodes.append(new_node)
            output_socket.input_nodes.append(new_node)
            clone.nodes.add(new_node)

        for subnet in self.subnets:
            new_subnet = subnet.copy(subnet.input_sockets, subnet.output_sockets)
            clone.nodes |= new_subnet.nodes
            clone.sockets |= new_subnet.sockets

        return clone

    def randomize(self):
        for node in self.nodes:
            node.randomize()



class InvalidSocket(Exception):

    def __str__(self):
        return repr()