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

	/*
	* Define the input of the network (in the input buffer of the first node)
	* This function do a blocking cudaMemCpy.
	*/
	void setInput(DTYPE const * buffer);

	/*
	* Retrieve the current output of the network (the data in the output buffer of the last node)
	* This function do a blocking cudaMemCpy
	*/
	void getOutput(DTYPE * buffer);

	/*
	* Return the size of the input buffer
	*/
	uint32_t getInputSize();

	/*
	* Return the size of the output buffer
	*/
	uint32_t getOutputSize();

	/*
	* Load a network on the device described by the NNetworkDescriptor.
	* Allocate and init the network on GPU memory. 
	*/
	cudaError_t loadNetwork(const NNetworkDescriptor& network);

	/*
	* Run a propagation phase on the device.
	*/
	void propagation();

	/*
	* Run a learning phase on the device.
	*/
	void learning(DTYPE const * expected, DTYPE alpha);

	/*
	* Synchronize the device (wait that all pending operation are performed)
	*/
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
