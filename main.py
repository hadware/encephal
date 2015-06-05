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

test_subnet = SubnetUnknownType.Unknown2(input_datasink,output_datasink)
#test_subnet = SubnetTopology.MLP1(input_datasink,output_datasink)
n = Network(test_subnet)

encoder = Onehot(output_datasink)
execute=Execute(learn_db,test_db,encoder)
execute.mean(n,1)








