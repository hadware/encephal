__author__ = 'lrx'

from execution.training.labeled_database import *
from execution.testing.labeled_database import *
from datasink.datasink import *
from nodes.math_function.math_function import *

"""
Class to execute and compute statistics on the performance of a network.
"""
class Execute:

    def __init__(self,learn_db,test_db,encoder):
        self.learn_db=learn_db
        self.test_db=test_db
        self.encoder=encoder


    def test(self,n):
        n.randomize()
        learning = TrainLabeledDatabase(n, self.learn_db, self.encoder, QuadraticError.differential)
        testing = TestLabeledDatabase(n, self.test_db, self.encoder)
        learning.online_learn(10000, 1)
        res=testing.test(False)
        return res


    def mean(self,n,nb_values):
        m=0
        for i in range(nb_values):
            res = self.test(n)
            print('value' + str(i) + ':' + str(res))
            m += res
        print("The average score value is:")
        print(m/nb_values)
