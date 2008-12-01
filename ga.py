#!/usr/bin/env python

# Genetic algorithm taken from:
#     P.C.Chu, J.E.Beasley.
#     Constraint Handling in Genetic Algorithms: The Set Partitioning Problem.
#     Journal of Heuristics, 11: 323--357 (1998)

from csp import CrewSchedulingProblem, namedtuple
from random import choice
from operator import attrgetter
from numpy import *
range = xrange

class Problem:
    # fields: A, c, alpha, beta
    def __init__(self, problem_file):
        csp = CrewSchedulingProblem(problem_file)
        columns, costs = [], []
        for rotation in csp.generate_rotations():
            column = zeros(len(csp.tasks), dtype='int8')
            for task in rotation.tasks:
                column[task] = 1
            columns.append(column)
            costs.append(rotation.cost)

        A = array(columns).transpose()
        c = array(costs)
        m, n = A.shape
        
        alpha = [set() for row in range(m)]
        beta =  [set() for col in range(n)]
        for row, cols in transpose(A.nonzero()):
            alpha[row].add(col)
            beta [col].add(row)

        self.A = A
        self.c = c
        self.alpha = alpha
        self.beta  = beta







    
   

    
def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] [input_file]")
    (options, args) = parser.parse_args()
    problem = Problem(open(args[0]))

if __name__ == '__main__':
    main()


