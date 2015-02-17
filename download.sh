#!/bin/bash
#TODO : Add decompression and make it python script
wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
mv train-images-idx3-ubyte.gz MNIST/
wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
mv train-labels-idx1-ubyte.gz MNIST/
wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
mv t10k-images-idx3-ubyte.gz MNIST/
wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
mv t10k-labels-idx1-ubyte.gz MNIST/