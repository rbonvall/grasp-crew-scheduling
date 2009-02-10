#!/usr/bin/env python

# Genetic algorithm taken from:
#     P.C.Chu, J.E.Beasley.
#     Constraint Handling in Genetic Algorithms: The Set Partitioning Problem.
#     Journal of Heuristics, 11: 323--357 (1998)

from csp import CrewSchedulingProblem, namedtuple
from random import choice
import numpy
from operator import attrgetter
range = xrange

class Problem:
    # fields: A, c
    def __init__(self, problem_file):
        csp = CrewSchedulingProblem(problem_file)
        columns, costs = [], []
        for rotation in csp.generate_rotations():
            column = numpy.zeros(len(csp.tasks), dtype='int8')
            for task in rotation.tasks:
                column[task] = 1
            columns.append(column)
            costs.append(rotation.cost)
        self.A = numpy.matrix(columns).transpose()
        self.costs = numpy.array(costs)

class Solution:
    __slots__ = ['columns', 'fitness', 'unfitness']
    def __init__(self, columns, problem):
        self.columns = numpy.array(columns).astype('int8')
        self.fitness = fitness(problem, self.columns)
        self.unfitness = unfitness(problem, self.columns)
    def __eq__(self, other):
        return (self.columns == other.columns).all()
    def __neq__(self, other):
        return not (self == other)
    def __repr__(self):
        return 'Solution(%s, f=%d, u=%d)' % (
                str.join('', map(str, columns)), self.fitness, self.unfitness)

def fitness(problem, solution):
    return numpy.dot(problem.costs, solution)

def unfitness(problem, solution):
    w = numpy.dot(problem.A, solution)
    return numpy.sum(numpy.abs(w - 1))


def construct_solution():
    # s = ...
    return Solution(s)


def binary_tournament(population):
    candidates = [choice(population), choice(population)]
    return min(candidates, key=attrgetter('fitness')) 

def most_compatible(population, P1):
    #P2 = ...
    return P2

def matching_selection(population):
    P1 = binary_tournament(population)
    if P1.unfitness == 0:
        P2 = binary_tournament(population)
    else:
        P2 = most_compatible(population, P1)
    return (P1, P2)

def uniform_crossover(P1, P2):
    mask = numpy.random.randint(2, size=P1.size)
    child = mask * P1.columns + (1 - mask) * P2.columns
    return Solution(child)

def mutation(solution, M_s, M_a, epsilon):
    return solution

def repair(solution):
    return solution
    
def ranking_replacement(population, solution):
    return

def best_solution(solutions):
    return solutions[0]

    

def ga(population_size, nr_iterations):
    population = [construct_solution() for k in range(population_size)]
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
    if not args:
        parser.print_help()
        return

    problem = Problem(open(args[0]))

if __name__ == '__main__':
    main()

