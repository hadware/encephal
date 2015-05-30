from scipy.cluster.hierarchy import leaders

__author__ = 'marechaux'

from subnet.network import *
from datasets.encoder.onehot import *
from datasets.MNIST import *
from test_options import *

learn_db = MNIST("training")
test_db = MNIST("testing")
input_datasink = learn_db.input_datasink
output_datasink = learn_db.output_datasink

test_subnet = Subnet()
FillSubnet.MLP(test_subnet,input_datasink,output_datasink)
n = Network(test_subnet)

encoder = Onehot(output_datasink)
statistic=Statistic(learn_db,test_db,encoder)
statistic.mean(n,1)








