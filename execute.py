__author__ = 'lrx'

from execution.training.labeled_database import *
from execution.testing.labeled_database import *
from datasink.datasink import *
from nodes.math_function.math_function import *
#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys import argv
import os
import csv
import matplotlib.pyplot as plt
import pylab
import json

from time import *
from subnet.network import *
from datasets.encoder.onehot import *
from datasets.MNIST import *
from subnet_architectures.fill_subnet import *
from subnet_architectures.subnet_topology import *
"""
Class to execute and compute statistics on the performance of a network.
"""
class Execute:

    def __init__(self,learn_db,test_db,encoder):
        self.learn_db=learn_db
        self.test_db=test_db
        self.encoder=encoder


    def test(self,network,nb_learn):
        network.randomize()
        learning = TrainLabeledDatabase(network, self.learn_db, self.encoder, QuadraticError.differential)
        testing = TestLabeledDatabase(network, self.test_db, self.encoder)
        learning.online_learn(nb_learn, 0.5 )
        res=testing.test(False)
        return res


    def mean(self,nb_learn,network,nb_values,print_bool = False):
        m=0
        for i in range(nb_values):
            res = self.test(network,nb_learn)
            if print_bool:
                print('value' + str(i) + ':' + str(res))
            m += res
        average = m/nb_values
        if print_bool:
            print("The average score value for " + str(nb_learn) + " learning samples is:" + str(average))
        return average

    #TODO: Define a real module to make graph with more abstraction, pouvant jouer sur vraiment beaucoup de paramètres facilement

    def print_txt_between_log(self,power10_a,power10_b,exposant,network,nb_values,changing_parameter,folder,print_bool = False):
        self.folder = folder
        self.output_filename = str(changing_parameter) + "_" + str(nb_values) + '.txt'
        x = []
        p = exposant**power10_a
        for i in range(power10_b - power10_a +1):
            x.append(p)
            p *= exposant
        print(x)
        self.print_txt(x,network,nb_values,print_bool)

    def print_txt_between_linear(self,a,b,nb_pts,network,nb_values,changing_parameter,folder,print_bool = False):
        self.folder = folder
        self.output_filename = str(changing_parameter) +   '_' +  str(nb_values)  + '.txt'
        x = []
        dt = (b-a) // nb_pts
        print(dt)
        for i in range(nb_pts+1):
            x.append(a+i*dt)
        print(x)
        self.print_txt(x,network,nb_values,print_bool)

    def print_txt(self,x,network,nb_values,print_bool):
        self.output_filename='graph/' + self.folder + self.output_filename

        print(os.path.isfile(self.output_filename))
        if os.path.isfile(self.output_filename):
            my_file = open(self.output_filename,'r')
            dictionnary = json.loads(my_file.read())
            my_file.close()
        else:
            dictionnary = dict()
        for i in x:
            debut = time()
            self.mean(i,network,nb_values,print_bool)
            fin = time()
            print(fin - debut)
            dictionnary[str(i)] = fin - debut
        print(dictionnary)
        my_file = open(self.output_filename,'w')
        my_file.write(json.dumps(dictionnary))
        my_file.close()

    def draw(self,title,filename_list,graph_number = 0):
        color_index = 0
        color_list = ['m','r','b','c','g','k','w','y']
        legend_list = [' Cuda 200','Cuda 5','Python 200','Python 5',]
        for filename in filename_list:
            #When files have a common begin and end for the filename
            begin_filename = 'graph/CudaSpeed/'
            end_filename = '_10.txt'
            print(begin_filename + filename + end_filename)
            file = open(begin_filename + filename + end_filename,'r')
            dic = json.loads(file.read())
            file.close()
            dic =  {int(k):float(v) for k,v in dic.items()}
            x = list(sorted(dic))
            y = []
            for i in x:
                y.append(dic[i])
            plt.plot(x,y,color_list[color_index],label = legend_list[color_index])

            color_index += 1


        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)
        plt.xlabel('Number of learning example chosen randomly for a test among 60000 samples')
        plt.ylabel('Time for learning in seconds')
        plt.xscale('log')
        plt.grid(True,which="both")
        output_filename = 'graph/CudaSpeed/' + title + '.png'
        plt.savefig(output_filename)
        plt.clf()
        plt.close()
