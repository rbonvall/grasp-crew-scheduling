#!/usr/bin/env python

# Genetic algorithm taken from:
#     P.C.Chu, J.E.Beasley.
#     Constraint Handling in Genetic Algorithms: The Set Partitioning Problem.
#     Journal of Heuristics, 11: 323--357 (1998)

from csp import CrewSchedulingProblem, namedtuple
from random import choice
from numpy import dot, zeros, array, matrix, random, sum, abs
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

    

def ga(problem, population_size=100, nr_iterations=1000):
    population = [construct_solution(problem) for k in range(population_size)]
    best_k = best_solution(population)
    for t in range(nr_iterations):
        p1, p2 = matching_selection(problem, population)
        child = uniform_crossover(population[p1], population[p2])
        child = mutation(child)
        child = repair(child)
        ranking_replacement(population, child)
        best_k = best_solution([best_solution, child])
    return population[best_k]

    
   

    
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

