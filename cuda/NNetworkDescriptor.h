#ifndef _NNETWORKDESCRIPTOR_H
#define _NNETWORKDESCRIPTOR_H

#include <vector>
#include <inttypes.h>
#include "encephal_alpha.pb.h"
#include "CudaType.h"

using namespace std;


class NNetworkDescriptor {
public:
	NNetworkDescriptor(){};
	NNetworkDescriptor(encephal_alpha::Graph &graph);

	
	/*
		id du buffers output de l'id de node en index
	*/
	vector<uint32_t> connection_out;
	
	/*
		id du buffers input de l'id de node en index
	*/
	vector<uint32_t> connection_in;

	/*
		Couches ordenencé des id des nodes
	*/
	vector<vector<uint32_t>> ordenecement_node;

	/*
		Taille de chaque buffers indexé par l'id des buffers
	*/
	vector<uint32_t> buffer_size;

	/*
		Type des nodes indexé par leurs id
	*/
	vector<type_node> nodes;
};


#endif
