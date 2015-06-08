__author__ = 'hadware'

from subnet.network import *
from datasets.encoder.onehot import *
from datasets.MNIST import *
from fill_subnet import *
from execute import *

# learn_db = MNIST("training")
# test_db = MNIST("testing")
# input_datasink = learn_db.input_datasink
# output_datasink = learn_db.output_datasink
#
# test_subnet = Subnet()
# FillSubnet.MLP(test_subnet, input_datasink, output_datasink)
# n = Network(test_subnet)
# with open("dump.graph", "wb") as file:
#     graph = n.to_protobuf_message()
#     graph
#     file.write(n.to_protobuf_message().SerializeToString())
#
# with open("dump.graph", "rb") as file:
#     graph = protobuf.Graph()
#     graph.ParseFromString(file.read())
#     print(graph)

with open("dump.graph", "wb") as file:
    graph = protobuf.Graph()
    graph.entry_socket = 0
    graph.exit_socket = 0
    file.write(graph.SerializeToString())
