__author__ = 'marechaux'

from datasink.socket import *
from nodes.node import *
from sys import maxsize

class Subnet(Node):
    """
    Represent a subnet which is a a space of storage with multiple input_node_sockets and output_node_sockets.

    Attributes:
    nodes (list node): Set of nodes present in the Subnet
    sockets (list sockets): Set of sockets present in the Socket
    """

    #TODO: si tout est recursif, vu que les constructions se font dans l'ordre on peut se permettre
    #TODO: de n'aller chercher les infos qu'à letage d en dessous

    def __init__(self):
        super().__init__()
        self.nodes = set()
        self.sockets = set()

    def is_subnet(self,node):
        return type(self) == type(node)

    def add_recursive_node(self,node):
        if not self.is_subnet(node):
            self.nodes.add(node)
        else:
            for intern_socket in node.sockets:
                self.sockets.add(intern_socket)
            for intern_node in node.nodes:
                self.add_recursive_node(intern_node)

    """ Functions on node, filling nodes attribut """

    def create_input(self,input_node):
        #Add nodes
        self.add_recursive_node(input_node)
        for input_node_socket in input_node.input_node_sockets:
            self.create_node_socket_input(input_node_socket)

    def create_output(self,output_node):
        #Add nodes
        self.add_recursive_node(output_node)
        for output_node_socket in output_node.output_node_sockets:
            self.create_node_socket_output(output_node_socket)

    def connect_nodes(self,left_node,right_node):
        if self.is_subnet(left_node) == self.is_subnet(right_node):
            #Add nodes
            self.add_recursive_node(left_node)
            self.add_recursive_node(right_node)
            #Connect the node sockets
            for i in range(len(left_node.output_node_sockets)):
                self.connect_node_sockets(left_node.output_node_sockets[i],right_node.input_node_sockets[i])
        else:
            print('Probleme: Impossible de connecter un Pipe_node et un subnet')

    """ Functions on node_socket, filling sockets attribut """

    def create_node_socket_input(self,input_node_socket):
        if not input_node_socket.connected_socket == None:
            #Add the existing socket
            self.sockets.add(input_node_socket.connected_socket)
        else:
            socket = Socket(input_node_socket.datasink)
            self.sockets.add(socket)
            #Linking after check
            input_node_socket.connect_socket(socket)
        #Add one input_node_socket for the subnet
        self.input_node_sockets.append(input_node_socket)

    def create_node_socket_output(self,output_node_socket):
        if not output_node_socket.connected_socket == None:
            #Add the existing socket
            self.sockets.add(output_node_socket.connected_socket)
        else:
            #Creation of the socket and add it
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
            #Linking after check
            output_node_socket.connect_socket(input_node_socket.connected_socket)
        elif output_node_socket.connected_socket != None  and input_node_socket.connected_socket == None:
            #Linking after check
            input_node_socket.connect_socket(output_node_socket.connected_socket)
        else:
        #they already have a socket between them, we have to merge
        #verifier que cela ne laisse pas un socket dans le vide ou quelque chose comme ca
        #(au pire celui qui n est pas garder est jeter par le garbage collector)
            print("merge")
            output_node_socket.connect_socket(input_node_socket.connected_socket)
            pass


    """ Scheduling """


    #TODO: check validity of the graph for complex case

    def schedule(self):
        unscheduled_sockets = list(self.sockets)

        for socket in unscheduled_sockets:
            socket.level = maxsize

        k = -1
        print("Verification")
        while unscheduled_sockets:
            k += 1
            for socket in unscheduled_sockets:
                candidate = True
                for node in socket.input_nodes:
                    if node.input_socket.level >= k:
                        candidate = False
                if candidate:
                    socket.level = k
                    unscheduled_sockets.remove(socket)

        self.sorted_node = []

        for i in range(k):
            self.sorted_node.append([])

        for node in self.nodes:
            self.sorted_node[node.input_socket.level].append(node)

        return self.sorted_node


    #TODO: realize different type of copies
    def copy_reference(self):
        return self;

    #Un type de copie , il va  y en avoir d'autres
    def copy2(self, input_translations = None, output_translations = None):
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