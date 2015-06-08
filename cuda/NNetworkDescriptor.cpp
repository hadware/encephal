#include "NNetworkDescriptor.h"

using namespace encephal_alpha;

NNetworkDescriptor::NNetworkDescriptor(Graph &graph) {
	buffer_size.resize(graph.sockets_size(), 0);

	/* On enregistre les tailles des buffers */
	for (int i = 0; i < graph.sockets_size(); i++) {
		DataType const &dataType = graph.sockets(i).datatype();
		
		/* Calcul de la dimension */
		uint32_t size = dataType.dimensions(0);
		for (int j = 1; j < dataType.dimensions_size(); j++)
			size *= dataType.dimensions(j);

		buffer_size[graph.sockets(i).index()] = size;
	}

	if(std::count(buffer_size.begin(), buffer_size.end(), 0) != 0)
		fprintf(stderr, "Warning : not all index of sockets are referenced.");

	uint32_t max_node_index = 0;
	ordenecement_node.resize(graph.node_layers_size(), std::vector<uint32_t>());
	
	for (int i = 0; i < graph.node_layers_size(); i++) {
		for (int j = 0; j < graph.node_layers(i).nodes_size(); j++) {
			PipeNode const &node = graph.node_layers(i).nodes(j);

			ordenecement_node[i] = std::vector<uint32_t>();
			ordenecement_node[i].push_back(node.index());

			max_node_index = max(max_node_index, node.index());
		}
	}

	connection_in.resize(max_node_index, 0);
	connection_out.resize(max_node_index, 0);
	nodes.resize(max_node_index, PERCEPTRON);

	if (std::count(connection_in.begin(), connection_in.end(), 0) != 0)
		fprintf(stderr, "Warning : not all index of nodes are referenced.");

	for (int i = 0; i < graph.node_layers_size(); i++) {
		for (int j = 0; j < graph.node_layers(i).nodes_size(); j++) {
			PipeNode const &node = graph.node_layers(i).nodes(j);
			connection_in[node.index()] = node.input_socket_index();
			connection_out[node.index()] = node.output_socket_index();
			
			switch (node.node_type()) {
			case PipeNode::PipeNodeType::PipeNode_PipeNodeType_FULL_CONNEXION:
				nodes[node.index()] = FCONNECTION;
				break;
			case PipeNode::PipeNodeType::PipeNode_PipeNodeType_PERCEPTRON_LAYER:
				if(node.data().perceptron_layer().activation_function() != ActivationFunction::SIGMOID)
					fprintf(stderr, "Warning : Unsupported activation function.");

				nodes[node.index()] = PERCEPTRON;
				break;
			default:
				fprintf(stderr, "Warning : Unsupported layer type.");
			}
		}
	}
}