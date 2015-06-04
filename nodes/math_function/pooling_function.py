__author__ = 'lrx'

from numpy import *
import itertools

class PoolingFunction:
    """Class that realize different type of pooling an a array such as max, average or L2 norm on local grids"""

    #TODO:Debeug and test the function
    def pool(self,input_data, output_shape, pooling_shape, stride_shape):
        output = zeros(output_shape)
        dim = output_shape.__len__()
        range_list = []
        index_input = []
        for d in dim:
            range_list.append(range(0,output_shape[d]))
            index_input.append(0)

        for index_output in tuple(itertools.product(*range_list)):
            for d in dim:
                index_input[d] = index_output[d] * stride_shape[d]
            slice_data = input_data
            for d in dim:
                slice_data = slice_data[slice(index_input[d],index_input[d] + pooling_shape[d],1)]
                slice_data = slice_data[0]
            output[index_output] = self.function_on_slice(slice_data)
        return output

    def pool_back(self):
        pass

    def function_on_slice(self,slice):
        pass

class MaxPooling(PoolingFunction):

    def function_on_slice(self,slice_array):
        return amax(slice_array)

class MeanPooling(PoolingFunction):

    def function_on_slice(self,slice_array):
        return average(slice_array)

class L2Pooling(PoolingFunction):
    pass


