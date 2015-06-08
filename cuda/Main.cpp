#include "encephal_alpha.pb.h"
#include "NNetworkDescriptor.h"
#include "CudaNetwork.h"

#include <iostream>    
#include <fstream>
#include <google/protobuf/stubs/common.h>


#define LEARNING_COEF 0.5

int performDataEntry(CudaNetwork &network, encephal_alpha::DataEntry const &entry)  {
	switch (entry.type()) {
	case encephal_alpha::DataEntry::DataEntryType::DataEntry_DataEntryType_TEST:
		if (!entry.has_testdataentry())
			return -1;
		
		network.setInput(entry.testdataentry().entries().float_vector().data());
		network.propagation();
		break;
	case encephal_alpha::DataEntry::DataEntryType::DataEntry_DataEntryType_TRAIN:
		if (!entry.has_traindataentry())
			return -1;

		network.setInput(entry.traindataentry().input().float_vector().data());
		network.learning(entry.traindataentry().label().float_vector().data(), LEARNING_COEF);
		
		break;
	}

	return 0;
}


int main(int argc, char *argv[]) {

	if (argc < 2) {
		fprintf(stderr, "Erreur spécifier un fichier de description de graphe en argument.");
		return -1;
	}

	std::filebuf fb;
	if (fb.open(argv[1], std::ios::in))
	{ 

		encephal_alpha::Graph graph;
		
		{
			std::istream is(&fb);
			if (!graph.ParseFromIstream(&is)){
				fprintf(stderr, "Erreur de parsage du fichier : \"%s\" format invalide ? (Protobuf version %7d)\n", argv[1], GOOGLE_PROTOBUF_VERSION);
				return -1;
			}
		}
		
		NNetworkDescriptor descriptor(graph);
		CudaNetwork network;
		network.loadNetwork(descriptor);

		encephal_alpha::DataEntry dataEntry;
		
		int size = 0;
		while (std::cin >> size) {
			char *buffer = new char[size];
			std::cin.read(buffer, size);

			if (dataEntry.ParseFromArray(buffer, sizeof(char))) {
				performDataEntry(network, dataEntry);
			}
			else {
				fprintf(stderr, "Erreur de parsage d'une donnée d'entré du réseau : format incompatible.\n");
			}

			delete[] buffer;
		}
	}
	else {
		fprintf(stderr, "Impossible d'ouvrir la description du graphe.\n");
		return -1;
	}
	

	return 0;
}