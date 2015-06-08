#include "CudaNetwork.h"
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <time.h>

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include "KernelNNetwork.h"

#define CUDAGPU_ID 0

#define CUDA_CHECK(a) do{cuda_check(a, __FILE__, __LINE__);}while(false)

void cuda_check(cudaError_t error, const char * file, int line) {
	if (error != cudaSuccess)
		printf("Cuda Error [%s/l.%d]: %s.\n", file, line, cudaGetErrorString(error));
}

void CudaNetwork::learning(DTYPE const * expected, DTYPE alpha) {
	CUDA_CHECK(cudaMemcpy(GPUexpected, expected, sizeof(DTYPE) * output_size, cudaMemcpyHostToDevice));
	//learningNoPipeline_AtomicKernelcall(GPUbuffer_tab, GPUFC_tab, GPUPCPTR_tab, node_type, index, buffer_size, node_number, GPUexpected, alpha);
	learningNoPipeline_kernelcall(GPUbuffer_tab, GPUnode_tab, GPUFC_tab, GPUPCPTR_tab, node_number, GPUexpected, alpha, maxdim);
}

void CudaNetwork::setInput(DTYPE const * buffer) {
	struct buffer_t buf;
	CUDA_CHECK(cudaMemcpy(&buf, GPUbuffer_tab, sizeof(struct buffer_t), cudaMemcpyDeviceToHost));
	CUDA_CHECK(cudaMemcpy(buf.propagation_valid, buffer, sizeof(DTYPE) * input_size, cudaMemcpyHostToDevice));
}

uint32_t CudaNetwork::getInputSize() {
	return input_size;
}

uint32_t CudaNetwork::getOutputSize() {
	return output_size;
}

void CudaNetwork::getOutput(DTYPE * buffer) {
	struct buffer_t buf;
	CUDA_CHECK(cudaMemcpy(&buf, GPUbuffer_tab + node_number, sizeof(struct buffer_t), cudaMemcpyDeviceToHost));
	CUDA_CHECK(cudaMemcpy(buffer, buf.propagation_valid, sizeof(DTYPE) * output_size, cudaMemcpyDeviceToHost));
}

void CudaNetwork::propagation() {
	propagationNoPipeline_AtomicKernelcall(GPUbuffer_tab, GPUFC_tab, GPUPCPTR_tab, node_type, index, buffer_size, node_number);
	//propagationNoPipeline_kernelcall(node_number, maxdim, GPUbuffer_tab, GPUnode_tab, GPUFC_tab, GPUPCPTR_tab);
}

cudaError_t CudaNetwork::loadNetwork(const NNetworkDescriptor& network) {
	cudaError_t cudaReturn = initDevice();
	if (cudaReturn != cudaSuccess)
		return cudaReturn;
	cudaReturn = allocNetwork(network);
	if (cudaReturn != cudaSuccess)
		return cudaReturn;
	cudaReturn = initNetwork(network);
	return cudaReturn;
}

cudaError_t CudaNetwork::initDevice() {
	cudaError_t cudaStatus = cudaSetDevice(CUDAGPU_ID);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "cudaSetDevice failed!  Do you have a CUDA-capable GPU installed?");
	}
	return cudaStatus;
};

void CudaNetwork::wait_finish() {
	CUDA_CHECK(cudaDeviceSynchronize());
}

cudaError_t CudaNetwork::allocNetwork(const NNetworkDescriptor& network) {

	node_number = network.nodes.size();
	int buffer_number = network.buffer_size.size();

	CUDA_CHECK(cudaMalloc((void**)&GPUbuffer_tab, sizeof(buffer) * buffer_number));
	CUDA_CHECK(cudaMalloc((void**)&GPUnode_tab, sizeof(node) * node_number));
	
	uint32_t num_FC = std::count(network.nodes.begin(), network.nodes.end(), FCONNECTION);
	
	CUDA_CHECK(cudaMalloc((void**)&GPUFC_tab, sizeof(FC) * num_FC));

	uint32_t num_PCPTR = std::count(network.nodes.begin(), network.nodes.end(), PERCEPTRON);
	CUDA_CHECK(cudaMalloc((void**)&GPUPCPTR_tab, sizeof(PCPTR) * num_PCPTR));

	return cudaGetLastError();
}

cudaError_t CudaNetwork::initNetwork(const NNetworkDescriptor& network) {
	assert(node_number && GPUbuffer_tab && GPUnode_tab && GPUPCPTR_tab && GPUFC_tab);
	
	/* on sauvegarde */
	buffer_size = network.buffer_size;
	node_type = network.nodes;

	input_size = network.buffer_size[0];
	output_size = network.buffer_size[network.buffer_size.size() - 1];;

	for (uint32_t i = 0; i < network.buffer_size.size(); i++) {
		uint32_t size = network.buffer_size[i];
		maxdim = (maxdim < size ? size : maxdim);
		DTYPE *propagation_valid, *propagation_calculated, *back_propagation;
		CUDA_CHECK(cudaMalloc((void**)&propagation_valid, sizeof(DTYPE) * size));
		CUDA_CHECK(cudaMalloc((void**)&propagation_calculated, sizeof(DTYPE) * size));
		CUDA_CHECK(cudaMalloc((void**)&back_propagation, sizeof(DTYPE) * size));

		buffer buf;
		buf.size = size;
		buf.back_propagation = back_propagation;
		buf.propagation_valid = propagation_valid;
		buf.propagation_calculated = propagation_calculated;

		CUDA_CHECK(cudaMemcpy(&(GPUbuffer_tab[i]), &buf, sizeof(buffer), cudaMemcpyHostToDevice));
	}
	uint32_t indiceFC = 0;
	uint32_t indicePCPTR = 0;
	srand((uint32_t)time(NULL));

	for (uint32_t i = 0; i < network.nodes.size(); i++) {
		node buf_node;
		buf_node.type = network.nodes[i];
		buf_node.indice = (buf_node.type == PERCEPTRON ? indicePCPTR : indiceFC);
		
		CUDA_CHECK(cudaMemcpy(&(GPUnode_tab[i]), &buf_node, sizeof(node), cudaMemcpyHostToDevice));
		
		if (buf_node.type == PERCEPTRON) {
			PCPTR pcptr;
			CUDA_CHECK(cudaMalloc((void**)&(pcptr.bias), sizeof(DTYPE) * network.buffer_size[i]));
		
			DTYPE * data = (DTYPE*)malloc(sizeof(DTYPE) * network.buffer_size[i]);
			assert(data);

			for (uint32_t j = 0; j < network.buffer_size[i]; j++) {
				data[j] = 0.01f * (rand() / (float)RAND_MAX - 0.005f);
			}
			CUDA_CHECK(cudaMemcpy(pcptr.bias, data, network.buffer_size[i] * sizeof(DTYPE), cudaMemcpyHostToDevice));
			free(data);

			CUDA_CHECK(cudaMemcpy(&(GPUPCPTR_tab[indicePCPTR]), &pcptr, sizeof(PCPTR), cudaMemcpyHostToDevice));

			index.push_back(indicePCPTR);
			indicePCPTR++;
		}
		else {
			FC fc;
			CUDA_CHECK(cudaMalloc((void**)&(fc.matrix), sizeof(DTYPE) * network.buffer_size[i] * network.buffer_size[i + 1]));
			
			DTYPE * data = (DTYPE*)malloc(sizeof(DTYPE) * network.buffer_size[i] * network.buffer_size[i+1]);
			assert(data);

			for (uint32_t j = 0; j < network.buffer_size[i] * network.buffer_size[i + 1]; j++) {
				data[j] = 0.01f * (rand() / (float)RAND_MAX - 0.005f);
			}
			CUDA_CHECK(cudaMemcpy(fc.matrix, data, network.buffer_size[i] * network.buffer_size[i + 1] * sizeof(DTYPE), cudaMemcpyHostToDevice));
			free(data);

			CUDA_CHECK(cudaMemcpy(&(GPUFC_tab[indiceFC]), &fc, sizeof(PCPTR), cudaMemcpyHostToDevice));
			index.push_back(indiceFC);
			indiceFC++;
		}
	}
	uint32_t countFC = std::count(network.nodes.begin(), network.nodes.end(), FCONNECTION);
	assert(indiceFC == countFC && indicePCPTR + indiceFC == network.nodes.size());

	CUDA_CHECK(cudaMalloc((void**)&GPUexpected, sizeof(DTYPE) * output_size));

	return cudaSuccess;
};