#ifndef _CUDA_NETWORK_H
#define _CUDA_NETWORK_H

#include <inttypes.h>
#include "NNetworkDescriptor.h"
#include "cuda_runtime.h"

#define DTYPE float

typedef struct buffer_t {
	uint32_t size;
	DTYPE * propagation_calculated;
	DTYPE * propagation_valid;
	DTYPE * back_propagation;
} buffer;


typedef struct node_t {
	type_node type;
	uint32_t indice;
} node;

typedef struct FC_t {
	DTYPE * matrix;
} FC;

typedef struct PCPTR_t {
	DTYPE * bias;
} PCPTR;

class CudaNetwork {
public:
	CudaNetwork(){};
	virtual ~CudaNetwork(){};

	void setInput(DTYPE const * buffer);
	uint32_t getInputSize();
	uint32_t getOutputSize();
	void getOutput(DTYPE * buffer);
	cudaError_t loadNetwork(const NNetworkDescriptor& network);

	void propagation();
	void learning(DTYPE const * expected, DTYPE alpha);

	void wait_finish();


private:
	CudaNetwork& operator=(const CudaNetwork& other) = delete;

	uint32_t input_size = 0;
	uint32_t output_size = 0;

	uint32_t node_number = 0;
	uint32_t maxdim = 0;
	std::vector<uint32_t> buffer_size;
	std::vector<type_node> node_type;
	std::vector<uint32_t> index;
	buffer * GPUbuffer_tab = NULL;
	node * GPUnode_tab = NULL;
	FC * GPUFC_tab = NULL;
	PCPTR * GPUPCPTR_tab = NULL;

	DTYPE * GPUexpected = NULL;

	cudaError_t allocNetwork(const NNetworkDescriptor& network);
	cudaError_t initNetwork(const NNetworkDescriptor& network);
	cudaError_t initDevice();
};


#endif