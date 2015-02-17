__author__ = 'marechaux'

from subnet.graph import *


class Subnet:

    def __init__(self):
        self.input_sockets = []
        self.output_sockets = []
        self.input_sizes = []
        self.output_size = []
        self.nodes = set()
        self.subnets = set()
        self.sockets = set()

    def add_input(self, size):
        socket = self.new_socket(size)
        self.input_sockets.append(socket)
        self.input_sizes.append(size)
        return socket

    def add_output(self, node, input = None):
        input_socket, output_socket = self.add_node(node, input)
        self.output_sockets.append(output_socket)
        self.output_size.append(output_socket.size)
        return input_socket

    def add_node(self, node, input_socket = None, output_socket = None):
        try:
            input = self.get_socket(input_socket, node.input_size, True)
        except InvalidSocket as e:
            raise ValueError("input_socket must be Socket or (Socket, Socket) or [Socket]")

        try:
            output = self.get_socket(output_socket, node.output_size, False)
        except InvalidSocket as e:
            raise ValueError("output_socket must be Socket or (Socket, Socket) or [Socket]")

        self.nodes.add(GraphNode(node, input, output))
        return input, output

    def add_subnet(self, subnet, input_sockets = None, output_sockets = None):
        # TODO: check non recusive
        try:
            input = self.get_socket_list(input_sockets, subnet.input_sizes, True)
        except InvalidSocket as e:
            raise ValueError("input_sockets must be ....")

        try:
            output = self.get_socket_list(output_sockets, subnet.output_sizes, False)
        except InvalidSocket as e:
            raise ValueError("output_sockets must be ....")

        graph_subnet = GraphSubnet(subnet, input, output)
        self.subnets.add(graph_subnet)
        return input, output

    def new_socket(self, size):
        socket = Socket(size)
        self.sockets.add(socket)
        return socket

    def as_input(self, socket):
        if socket is None:
            raise ValueError("socket must be not null")
        elif socket not in self.sockets:
            raise ValueError("socket must be already in the subnet")
        elif socket in self.input_sockets:
            raise ValueError("socket must not be already in the subnet outputs")
        else:
            input = self.get_socket(socket, None, False)
            self.input_sockets.append(input)
            self.input_sizes.append(input.size)

    def as_output(self, socket):
        if socket is None:
            raise ValueError("socket must be not null")
        elif socket not in self.sockets:
            raise ValueError("socket must be already in the subnet")
        elif socket in self.output_sockets:
            raise ValueError("socket must not be already in the subnet inputs")
        else:
            output = self.get_socket(socket, None, False)
            self.output_sockets.append(output)
            self.output_sockets.append(output.size)

    def get_socket(self, socket, size, is_input):
        #TODO : Check the socket exist in the subnet
        if socket is None:
            return self.new_socket(size)
        elif type(socket) is tuple: #TODO : Check type in the tuple
            if is_input:
                return socket[1]
            else:
                return socket[0]
        elif type(socket) is (list, list):
            if is_input:
                return self.get_socket(socket[1], is_input)
            else:
                return self.get_socket(socket[0], is_input)
        elif type(socket) is Socket:
            return socket
        elif type(socket) is list and socket.size == 1 and type(socket[0]) is Socket:
            return socket[0]
        else:
            print(type(socket))
            raise InvalidSocket()

    def get_socket_list(self, sockets, sockets_signature, is_input):
        if sockets is None:
            result = []
            for i, element in enumerate(sockets_signature):
                result.append(self.new_socket(sockets_signature(i)))
            return result
        elif type(sockets) is not list and len(sockets_signature) == 1:
            return [self.get_socket(sockets, sockets_signature[0], is_input)]
        elif type(sockets) is list and len(sockets) == len(sockets_signature):
            result = []
            for i, element in enumerate(sockets_signature):
                result.append(self.get_socket(sockets[i], element, is_input))
            return result
        else:
            raise InvalidSocket()

    #Un type de copie , il vas y en avoir d'autres
    def copy(self, input_translations = None, output_translations = None):
        clone = Subnet()

        socket_translator = {}

        if input_translations is not None:
            for i, input_socket in enumerate(input_translations):
                socket_translator[self.input_sockets[i]] = input_socket
        else:
            for input_socket in self.input_sockets:
                new_input_socket = Socket(input_socket.size)
                socket_translator[input_socket] = new_input_socket
                clone.sockets.add(new_input_socket)
                clone.input_sockets.append(new_input_socket)

        if output_translations is not None:
            for i, output_socket in enumerate(output_translations):
                socket_translator[self.output_sockets[i]] = output_socket
        else:
            for output_socket in self.output_sockets:
                new_output_socket = Socket(output_socket.size)
                socket_translator[output_socket] = new_output_socket
                clone.sockets.add(new_output_socket)
                clone.output_sockets.append(new_output_socket)


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



class InvalidSocket(Exception):

    def __str__(self):
        return repr()