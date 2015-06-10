__author__ = 'marechaux'

from subnet.network import *
from datasets.encoder.onehot import *
from datasets.MNIST import *
from subnet_architectures.fill_subnet import *
from subnet_architectures.subnet_topology import *
from subnet_architectures.subnet_unknownType import *
from execute import *

learn_db = MNIST("training")
test_db = MNIST("testing")
input_datasink = learn_db.input_datasink
output_datasink = learn_db.output_datasink

#test_subnet = SubnetUnknownType.Unknown1(input_datasink,output_datasink)
'''hidden_size = 10
nb_layer = 4
test_subnet = SubnetTopology.DeepMLP(input_datasink,output_datasink,hidden_size,nb_layer)'''
n = 5
L = 1
p = 1
dropout = 1
test_subnet = SubnetTopology.MLP1(input_datasink,output_datasink,n,L,p,0)
network = Network(test_subnet)

encoder = Onehot(output_datasink)
execute=Execute(learn_db,test_db,encoder)
#execute.mean(10000,network,3,True)

case = 2
if case == 1:
    execute.print_txt_between_linear(2700,2700,1,network,1,n,'CudaSpeed/',True)
    execute.print_txt_between_linear(1700,1700,1,network,1,n,'CudaSpeed/',True)
    execute.print_txt_between_linear(1000,5000,4,network,1,n,'CudaSpeed/',True)
    execute.print_txt_between_linear(10000,60000,5,network,1,n,'CudaSpeed/',True)
elif case == 2:
    filename_list = ['cuda_200','cuda_5','py_200','py_5',]
    execute.draw('CudaSpeed',filename_list)
else:
    None








