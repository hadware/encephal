#ifndef KERNELNNETWORK_H
#define KERNELNNETWORK_H

void propagationNoPipeline_kernelcall(int node_number, int maxdim, buffer * GPUbuffer_tab, node *GPUnode_tab, FC *GPUFC_tab, PCPTR *GPUPCPTR_tab);
void propagation_kernelcall(int node_number, int maxdim, buffer * GPUbuffer_tab, node *GPUnode_tab, FC *GPUFC_tab, PCPTR *GPUPCPTR_tab);
void learningNoPipeline_kernelcall(buffer * buffers, node * nodes, FC * fc, PCPTR * pcptr, int node_size, float * expected, DTYPE alpha, int maxdim);
void propagationNoPipeline_AtomicKernelcall(buffer * buffers, FC * fc, PCPTR * pcptr, std::vector<type_node> &node_type, std::vector<uint32_t> &index, std::vector<uint32_t> &buffer_size, int node_number);
void learningNoPipeline_AtomicKernelcall(buffer * buffers, FC * fc, PCPTR * pcptr, std::vector<type_node> &node_type, std::vector<uint32_t> &index, std::vector<uint32_t> &buffer_size, int node_number, DTYPE * expected, DTYPE alpha);

#endif