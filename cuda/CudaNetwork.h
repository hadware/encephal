#ifndef _CUDA_NETWORK_H
#define _CUDA_NETWORK_H

#include "NNetworkDescriptor.h"
#include "cuda_runtime.h"

#include "CudaType.h"

class CudaNetwork {
public:
	CudaNetwork() : input_size(0), output_size(0),
    node_number(0), maxdim(0), GPUbuffer_tab(NULL), GPUnode_tab(NULL), GPUFC_tab(NULL), GPUPCPTR_tab(NULL), GPUexpected(NULL) {};
	
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

	uint32_t input_size;
	uint32_t output_size;

	uint32_t node_number;
	uint32_t maxdim;
	std::vector<uint32_t> buffer_size;
	std::vector<type_node> node_type;
	std::vector<uint32_t> index;
	buffer * GPUbuffer_tab;
	node * GPUnode_tab;
	FC * GPUFC_tab;
	PCPTR * GPUPCPTR_tab;

	DTYPE * GPUexpected;

	cudaError_t allocNetwork(const NNetworkDescriptor& network);
	cudaError_t initNetwork(const NNetworkDescriptor& network);
	cudaError_t initDevice();
};


#endif
