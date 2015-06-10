#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include "device_functions.h"
#include <vector>

#ifndef __CUDACC__
#define __CUDACC__
#endif
#include "CudaType.h"

#define SHAREDSIZE ((16 * 1024)/sizeof(DTYPE))

extern __device__ void __syncthreads();

__global__ void kernelBuffer_propagation(buffer * buffers) {
	int id_buf = blockIdx.x;
	int id_coord = threadIdx.x;

	buffers[id_buf].propagation_valid[id_coord] = buffers[id_buf].propagation_calculated[id_coord];
}

__device__ void propagation_perceptron(buffer * input, buffer * output, PCPTR * perceptron) {
	int id = threadIdx.x;
	if (id < input->size)
		output->propagation_calculated[id] = ((DTYPE)1) / (1 + exp(-input->propagation_valid[id] - perceptron->bias[id]));
}
__device__ void propagation_fullconnection(buffer * input, buffer * output, FC * fconnection) {
	int id = threadIdx.x;
	__shared__ DTYPE input_buffer[SHAREDSIZE];
	int size_output = output->size;
	int size_input = input->size;
	if (id < size_input) {
		input_buffer[id] = input->propagation_valid[id];
		__syncthreads();
		DTYPE resultat = input_buffer[0] * fconnection->matrix[id * size_output];
		for (int i = 1; i < size_input; i++)
			resultat += input_buffer[i] * fconnection->matrix[id * size_output + i];

		output->propagation_calculated[id] = resultat;
	}
}
__global__ void kernelNetwork_propagation(buffer * buffers, node * nodes, FC * fc, PCPTR * pcptr) {
	int layer = blockIdx.x;
	buffer * input = buffers + layer;
	buffer * output = input + 1;

	switch (nodes[layer].type) {
	case PERCEPTRON:
		propagation_perceptron(input, output, pcptr + nodes[layer].indice);
		break;
	case FCONNECTION:
		propagation_fullconnection(input, output, fc + nodes[layer].indice);
		break;
	}
}

void propagation_kernelcall(int node_number, int maxdim, buffer * GPUbuffer_tab, node *GPUnode_tab, FC *GPUFC_tab, PCPTR *GPUPCPTR_tab) {
	kernelNetwork_propagation<<<node_number, maxdim>>>(GPUbuffer_tab, GPUnode_tab, GPUFC_tab, GPUPCPTR_tab);
	kernelBuffer_propagation<<<node_number + 1, maxdim>>>(GPUbuffer_tab);
}

__device__ void fullconnection_propagationNoPipeline(buffer * input, buffer * output, FC * fc) {
	int id = threadIdx.x;
	uint32_t input_size = input->size;
	uint32_t output_size = output->size;
	
	__shared__ DTYPE input_buffer[SHAREDSIZE];
	if (id < input_size)
		input_buffer[id % input_size] = input->propagation_valid[id % input_size];

	__syncthreads();

	if (id < output_size) {
		
		DTYPE resultat = input_buffer[0] * fc->matrix[id];
		for (uint32_t i = 1; i < input_size; i++) {
			resultat += input_buffer[i] * fc->matrix[id + output_size * i];
		}

		output->propagation_valid[id] = resultat;
	}
}
__device__ void perceptron_propagationNoPipeline(buffer * input, buffer * output, PCPTR * pcptr) {
	int id = threadIdx.x ;
	if (id < input->size)
		output->propagation_valid[id] = ((DTYPE)1) / (((DTYPE)1) + ((DTYPE)__expf(-input->propagation_valid[id] - pcptr->bias[id])));
}
__device__ void propagationNoPipeline(buffer * input, buffer * output, node * node, FC * fc, PCPTR * pcptr) {
	switch (node->type) {
	case PERCEPTRON:
		perceptron_propagationNoPipeline(input, output, &(pcptr[node->indice]));
		break;
	case FCONNECTION:
		fullconnection_propagationNoPipeline(input, output, &(fc[node->indice]));
		break;
	}
} 

__device__ void backpropagation_perceptron(buffer * input, buffer * output, PCPTR * node) {
	int id = threadIdx.x;
	if (id < input->size) {
		output->back_propagation[id] = input->back_propagation[id] * input->propagation_valid[id] * ((DTYPE)1 - input->propagation_valid[id]);
	}
}
__device__ void backpropagation_fullconnection(buffer * input, buffer * output, FC * node) {
	int id = threadIdx.x;
	__shared__ DTYPE input_buffer[SHAREDSIZE];
	int size_output = output->size;
	int size_input = input->size;

	if (id < size_input)
		input_buffer[id] = input->back_propagation[id];

	__syncthreads();

	if (id < size_output) {
		DTYPE resultat = input_buffer[0] * node->matrix[id * size_input];
		for (int i = 1; i < size_input; i++)
			resultat += input_buffer[i] * node->matrix[id * size_input + i];
	
		output->back_propagation[id] = resultat;
	}
}
__device__ void backPropagation(buffer * input, buffer * output, node * node, FC * fc, PCPTR * pcptr, int node_size) {
	switch (node->type) {
	case PERCEPTRON:
		backpropagation_perceptron(input, output, pcptr + node->indice);
		break;
	case FCONNECTION:
		backpropagation_fullconnection(input, output, fc + node->indice);
		break;
	}
}

__device__ void gradient(buffer * resultat, DTYPE * expected) {
	int id = threadIdx.x;
	if (id < resultat->size) {
		resultat->back_propagation[id] = resultat->propagation_valid[id] - expected[id];
	}
}

__global__ void gradient_kernel(buffer * resultat, DTYPE * expected) {
	int id = threadIdx.x;
	if (id < resultat->size) {
		resultat->back_propagation[id] = resultat->propagation_valid[id] - expected[id];
	}
}

__device__ void learn_perceptron(buffer * input, buffer * output, PCPTR * pcptr, DTYPE alpha) {
	int id = threadIdx.x;
	if (id < input->size)
		pcptr->bias[id] -= alpha * input->back_propagation[id];
}
__device__ void learn_fullconnection(buffer * input, buffer * output, FC * fc, DTYPE alpha) {
	int input_size = input->size;
	int output_size = output->size;

	int id = threadIdx.x ;
	
	__shared__ DTYPE input_prop[SHAREDSIZE / 2];
	__shared__ DTYPE output_backprop[SHAREDSIZE / 2];
	

	if (id < output_size)
		output_backprop[id] = output->back_propagation[id];

	if (id < input_size)
		input_prop[id % input_size] = input->propagation_valid[id % input_size];

	__syncthreads();
	if (id < output_size)
		for (int i = 0; i < input_size; i++)
			fc->matrix[id + output_size * i] -= alpha * input_prop[i] * output_backprop[id];
}
__device__ void learn(buffer * input, buffer * output, node * node, FC * fc, PCPTR * pcptr, DTYPE alpha) {
	switch (node->type) {
	case PERCEPTRON:
		learn_perceptron(input, output, pcptr + node->indice, alpha);
		break;
	case FCONNECTION:
		learn_fullconnection(input, output, fc + node->indice, alpha);
		break;
	}
}

__global__ void kernelNetwork_learningNoPipeline(buffer buffers[], node nodes[], FC fc[], PCPTR pcptr[], int node_size, float * expected, DTYPE alpha) {
	//propagation
	for (uint32_t i = 0; i < node_size; i++) {
		propagationNoPipeline(&(buffers[i]), &(buffers[i + 1]), &(nodes[i]), fc, pcptr);
		__syncthreads();
	} 
	//gradient
	gradient(buffers + node_size, expected);
	__syncthreads();

	//backpropagation
	for (int32_t i = node_size - 1; i >= 0; i--) {
		backPropagation(buffers + i + 1, buffers + i, nodes + i, fc, pcptr, node_size);
		__syncthreads();
	}

	//apprentissage
	for (uint32_t i = 0; i < node_size; i++) {
		learn(buffers + i, buffers + i + 1, nodes + i, fc, pcptr, alpha);
		__syncthreads();
	}
}

__global__ void kernelNetwork_propagationNoPipeline(buffer * buffers, node *nodes, FC *fc, PCPTR *pcptr, int node_size) {
	for (uint32_t i = 0; i < node_size; i++) {
		propagationNoPipeline(buffers + i, buffers + i + 1, nodes + i, fc, pcptr);
		__syncthreads();
	}
}

__global__ void kernelPerceptronLayer_propagation(buffer *input, buffer *output, PCPTR *node) {
	int id = threadIdx.x;
	output->propagation_valid[id] = ((DTYPE)1) / (((DTYPE)1) + ((DTYPE)__expf(-input->propagation_valid[id] - node->bias[id])));
}
__global__ void kernelFullConnection_propagation(buffer *input, buffer *output, FC *node) {
	int id = threadIdx.x;
	uint32_t input_size = input->size;
	uint32_t output_size = output->size;

	//__shared__ DTYPE input_buffer[SHAREDSIZE];

	//input_buffer[id] = input->propagation_valid[id];

	__syncthreads();

	/*A paraleliser*/
	DTYPE resultat = input->propagation_valid[0] * node->matrix[id];
	for (uint32_t i = 1; i < input_size; i++) {
		resultat += input->propagation_valid[i] * node->matrix[id + output_size * i];
	}

	output->propagation_valid[id] = resultat;
}

__global__ void kernelPerceptronLayer_backpropagation(buffer *input, buffer *output, PCPTR *node) {
	int id = threadIdx.x;
	output->back_propagation[id] = input->back_propagation[id] * input->propagation_valid[id] * ((DTYPE)1 - input->propagation_valid[id]);
}
__global__ void kernelFullConnection_backpropagation(buffer *input, buffer *output, FC *node) {
	int id = threadIdx.x;
	//__shared__ DTYPE input_buffer[SHAREDSIZE];
	//int size_output = output->size;
	int size_input = input->size;

	//int id_output = id % size_output;

	//if (id < size_input)
//	input_buffer[id % size_input] = input->back_propagation[id % size_input];

	__syncthreads();

	//if (id < size_output) {
	DTYPE resultat = input->back_propagation[0] * node->matrix[id * size_input];
	for (int i = 1; i < size_input; i++)
		resultat += input->back_propagation[i] * node->matrix[id * size_input + i];

	output->back_propagation[id] = resultat;

}

__global__ void kernelPerceptronLayer_learning(buffer * input, buffer * output, PCPTR * pcptr, DTYPE alpha) {
	int id = threadIdx.x;
	pcptr->bias[id] -= alpha * input->back_propagation[id];
}
__global__ void kernelFullConnection_learning(buffer * input, buffer * output, FC * fc, DTYPE alpha) {
	int input_size = input->size;
	int output_size = output->size;

	int id = threadIdx.x;
	/*
	__shared__ DTYPE input_prop[SHAREDSIZE / 2];
	__shared__ DTYPE output_backprop[SHAREDSIZE / 2];


	if (id < output_size)
		output_backprop[id] = output->back_propagation[id];

	if (id < input_size)
		input_prop[id % input_size] = input->propagation_valid[id % input_size];

	__syncthreads();
	if (id < output_size)*/
		for (int i = 0; i < input_size; i++)
			fc->matrix[id + output_size * i] -= alpha * input->propagation_valid[i] * output->back_propagation[id];
}


void propagationNoPipeline_kernelcall(int node_number, int maxdim, buffer * GPUbuffer_tab, node *GPUnode_tab, FC *GPUFC_tab, PCPTR *GPUPCPTR_tab) {
	kernelNetwork_propagationNoPipeline << <1, maxdim >> >(GPUbuffer_tab, GPUnode_tab, GPUFC_tab, GPUPCPTR_tab, node_number);
}

void learningNoPipeline_kernelcall(buffer * buffers, node * nodes, FC * fc, PCPTR * pcptr, int node_size, float * expected, DTYPE alpha, int maxdim) {
	kernelNetwork_learningNoPipeline <<<1, maxdim>>>(buffers, nodes, fc, pcptr, node_size, expected, alpha);
}

/*
	il faut que buffer soit decroissant
*/
void propagationNoPipeline_AtomicKernelcall(
	buffer * buffers, FC * fc, PCPTR * pcptr, 
	std::vector<type_node> &node_type, std::vector<uint32_t> &index, 
	std::vector<uint32_t> &buffer_size, int node_number) {
	
	for (int i = 0; i < node_number; i++) {
		switch (node_type[i]) {
		case FCONNECTION:
			//printf("kernel call : FC\n");
			kernelFullConnection_propagation <<<1, buffer_size[i + 1] >> >(buffers + i, buffers + i + 1, fc + index[i]);
			break;
		case PERCEPTRON:
			//printf("kernel call : PERCEP\n");
			kernelPerceptronLayer_propagation <<<1, buffer_size[i + 1] >> >(buffers + i, buffers + i + 1, pcptr + index[i]);
			break;
		}
	}
}

void learningNoPipeline_AtomicKernelcall(
	buffer * buffers, FC * fc, PCPTR * pcptr,
	std::vector<type_node> &node_type, std::vector<uint32_t> &index,
	std::vector<uint32_t> &buffer_size, int node_number, DTYPE * expected, DTYPE alpha) {
	
	propagationNoPipeline_AtomicKernelcall(buffers, fc, pcptr, node_type, index, buffer_size, node_number);

	gradient_kernel << <1, buffer_size[node_number] >> >(buffers + node_number, expected);

	for (int i = node_number - 1; i >= 0; i--) {
		switch (node_type[i]) {
		case FCONNECTION:
			//printf("kernel call : FC\n");
			kernelFullConnection_backpropagation << <1, buffer_size[i] >> >(buffers + i + 1, buffers + i, fc + index[i]);
			break;
		case PERCEPTRON:
			//printf("kernel call : PERCEP\n");
			kernelPerceptronLayer_backpropagation << <1, buffer_size[i] >> >(buffers + i + 1, buffers + i, pcptr + index[i]);
			break;
		}
	}

	for (int i = 0; i < node_number; i++) {
		switch (node_type[i]) {
		case FCONNECTION:
			//printf("kernel call : FC\n");
			kernelFullConnection_learning <<<1, buffer_size[i + 1] >> >(buffers + i + 1, buffers + i, fc + index[i], alpha);
			break;
		case PERCEPTRON:
			//printf("kernel call : PERCEP\n");
			kernelPerceptronLayer_learning <<<1, buffer_size[i + 1] >> >(buffers + i + 1, buffers + i, pcptr + index[i], alpha);
			break;
		}
	}
}
