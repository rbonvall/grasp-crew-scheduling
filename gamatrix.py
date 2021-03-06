#!/usr/bin/env python

# Genetic algorithm taken from:
#     P.C.Chu, J.E.Beasley.
#     Constraint Handling in Genetic Algorithms: The Set Partitioning Problem.
#     Journal of Heuristics, 11: 323--357 (1998)

from csp import CrewSchedulingProblem, namedtuple, frozenset
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
            column = zeros(len(csp.tasks), dtype='uint8')
            for task in rotation.tasks:
                column[task] = 1
            columns.append(column)
            costs.append(rotation.cost)

        A = array(columns).transpose()
        m, n = A.shape
        
        alpha = [set() for row in range(m)]
        beta =  [set() for col in range(n)]
        for row, col in transpose(A.nonzero()):
            alpha[row].add(col)
            beta [col].add(row)

        self.A = A
        self.rotation_costs = array(costs)
        self.nr_rows, self.nr_cols = m, n
        self.alpha = map(frozenset, alpha)
        self.beta  = map(frozenset, beta)

    def __repr__(self):
        return '<CSP problem, %dx%d>' % (self.nr_rows, self.nr_cols)


def initial_solution(problem, population_size=1):
    solution = zeros((problem.nr_cols, population_size), dtype='uint8')
    I = frozenset(range(problem.nr_rows))
    for k in range(population_size):
        S, U = set(), set(I)
        while U:
            i = choice(list(U))
            J = [j for j in problem.alpha[i] if not (problem.beta[j] & (I - U))]
            if J:
                j = choice(J)
                solution[j, k] = 1
                U -= problem.beta[j]
            else:
                U.remove(i)
    return solution


def ga(problem, nr_iterations=100, population_size=100):
    population = [initial_solution(problem, population_size)
                  for k in range(population_size)]
    best = best_solution(population)
    for t in range(nr_iterations):
        P1, P2 = matching_selection(population)
        C = uniform_crossover(P1, P2)
        C = mutation(C, M_s, M_a, epsilon)
        C = repair(C)
        ranking_replacement(population, C)
        best = best_solution([best_solution, C])
    return best


    
def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] [input_file]")
    (options, args) = parser.parse_args()
    problem = Problem(open(args[0]))

if __name__ == '__main__':
    main()


