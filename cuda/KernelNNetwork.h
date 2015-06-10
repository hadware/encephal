#ifndef KERNELNNETWORK_H
#define KERNELNNETWORK_H

#include "CudaType.h"

/*
* Call the kernels to do a complete phase of propagation (the propagation is handled by a kernel).
*/
void propagationNoPipeline_kernelcall(int node_number, int maxdim, buffer * GPUbuffer_tab, node *GPUnode_tab, FC *GPUFC_tab, PCPTR *GPUPCPTR_tab);

/*
* Call the kernels to do a single step of propagation on all the node.
*/
void propagation_kernelcall(int node_number, int maxdim, buffer * GPUbuffer_tab, node *GPUnode_tab, FC *GPUFC_tab, PCPTR *GPUPCPTR_tab);

/*
* Call the kernels to do a complete phase of learning  (the learning is handled by a kernel).
*/
void learningNoPipeline_kernelcall(buffer * buffers, node * nodes, FC * fc, PCPTR * pcptr, int node_size, float * expected, DTYPE alpha, int maxdim);

/*
* Call the kernels to do a complete phase of propagation (the propagation is handled by a loop on CPU).
*/
void propagationNoPipeline_AtomicKernelcall(buffer * buffers, FC * fc, PCPTR * pcptr, std::vector<type_node> &node_type, std::vector<uint32_t> &index, std::vector<uint32_t> &buffer_size, int node_number);

/*
* Call the kernels to do a complete phase of learning  (the learning is handled by a a loop on CPU).
*/
void learningNoPipeline_AtomicKernelcall(buffer * buffers, FC * fc, PCPTR * pcptr, std::vector<type_node> &node_type, std::vector<uint32_t> &index, std::vector<uint32_t> &buffer_size, int node_number, DTYPE * expected, DTYPE alpha);

#endif