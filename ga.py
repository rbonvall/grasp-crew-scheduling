#!/usr/bin/env python

# Genetic algorithm taken from:
#     P.C.Chu, J.E.Beasley.
#     Constraint Handling in Genetic Algorithms: The Set Partitioning Problem.
#     Journal of Heuristics, 11: 323--357 (1998)

from csp import CrewSchedulingProblem, namedtuple
from random import choice, randrange
from numpy import dot, zeros, array, matrix, random, sum, abs
from operator import attrgetter
range = xrange

class Problem:
    # fields: A, c
    def __init__(self, problem_file):
        csp = CrewSchedulingProblem(problem_file)
        columns, costs = [], []
        for rotation in csp.generate_rotations():
            column = zeros(len(csp.tasks), dtype='int8')
            for task in rotation.tasks:
                column[task] = 1
            columns.append(column)
            costs.append(rotation.cost)
        self.A = matrix(columns).transpose()
        self.costs = array(costs)
        self.nr_tasks, self.nr_rotations = self.A.shape

Solution = namedtuple('Solution', 'columns covering fitness unfitness')

def make_solution(problem, columns):
    covering = dot(problem.A, columns)
    fitness = dot(problem.costs, columns)
    unfitness = sum(abs(covering - 1))
    return Solution(columns, covering, fitness, unfitness)

def construct_solution(problem):
    # TODO: smarter solution construction
    columns = random.randint(2, size=problem.nr_rotations).astype('int8')
    return make_solution(problem, columns)

def binary_tournament(population):
    population_size = len(population)
    candidates = [randrange(population_size) for _ in range(2)]
    return min(candidates, key=lambda index: population[index].fitness)

def matching_selection(problem, population):
    '''Indices of the solutions selected for crossover.'''
    P1 = binary_tournament(population)
    if population[P1].unfitness == 0:
        P2 = binary_tournament(population)
    else:
        cols_P1 = population[P1].columns
        def compatibility(k):
            cols_Pk = population[k].columns
            comp = sum(cols_P1 | cols_Pk) - sum(cols_P1 & cols_Pk)
            return comp, population[P1].fitness  # use fitness to break ties
        P2 = max((k for k, sol in enumerate(population) if k != P1),
                 key=compatibility)
    return (P1, P2)

def uniform_crossover(parent1, parent2):
    '''Columns of the child after crossover.'''
    mask = random.randint(2, size=parent1.columns.size)
    return mask * parent1.columns + (1 - mask) * parent2.columns

def static_mutation(columns, M_s=3):
    for _ in range(M_s):
        j = randrange(columns.size)
        columns[j] = 1 - columns[j]
    return columns

def adaptive_mutation(columns, M_a=5, epsilon=0.5):
    return columns


def repair(solution):
    # ...
    return solution
    
def ranking_replacement(population, solution):
    # ...
    return

def best_solution(population):
    # ...
    return 0
    

def ga(problem, population_size=100, nr_iterations=1000):
    population = [construct_solution(problem) for k in range(population_size)]
    best_k = best_solution(population)
    for t in range(nr_iterations):
        p1, p2 = matching_selection(problem, population)
        child = uniform_crossover(population[p1], population[p2])
        child = static_mutation(child)
        child = adaptive_mutation(child)
        child = repair(child)
        ranking_replacement(population, child)
        best_k = best_solution([best_solution, child])
    return population[best_k]

    
   

    
def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] [input_file]")
    (options, args) = parser.parse_args()
    if not args:
        parser.print_usage()
        return

    problem = Problem(open(args[0]))
    print ga(problem)

if __name__ == '__main__':
    main()

