__author__ = 'hadware'

from svg_render.network_elements import Element, ElementType
from svg_render.fake_network import Network

#creating the nodes
input_node = Element(ElementType.NODE, "input")
first_connections = [Element(ElementType.CONNEXION, "c1"), Element(ElementType.SUBNET, "c2")]
hidden_nodes = [Element(ElementType.NODE, "n1"), Element(ElementType.NODE, "n2")]
second_connections = [Element(ElementType.SUBNET, "c3"), Element(ElementType.SUBNET, "c4")]
output_node = Element(ElementType.NODE, "output")

#linking them
input_node.add_connection(first_connections)

for i in range(1):
    first_connections[i].add_connection(hidden_nodes[i])
    hidden_nodes[i].add_connection(second_connections[i])
    second_connections[i].add_connection(output_node)
first_connections[1].add_connection([output_node, hidden_nodes[0]])
fake_network = Network(input_node, output_node)
fake_network.build_graph("test.svg")
