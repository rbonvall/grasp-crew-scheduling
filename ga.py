#!/usr/bin/env python

# Genetic algorithm taken from:
#     P.C.Chu, J.E.Beasley.
#     Constraint Handling in Genetic Algorithms: The Set Partitioning Problem.
#     Journal of Heuristics, 11: 323--357 (1998)

from csp import CrewSchedulingProblem, namedtuple
from random import choice
from numpy import array, random, equal
from numpy import random
from operator import attrgetter
range = xrange

class Solution:
    __slots__ = ['columns', 'fitness', 'unfitness']
    def __init__(self, columns):
        self.columns = array(columns).astype('int8')
        self.fitness = fitness(self.columns)
        self.unfitness = unfitness(self.columns)
    def __eq__(self, other):
        return (self.columns == other.columns).all()
    def __neq__(self, other):
        return not (self == other)
    def __repr__(self):
        return 'Solution(%s, f=%d, u=%d)' % (
                str.join('', map(str, columns)), self.fitness, self.unfitness)

def fitness(solution):
    pass
def unfitness(solution):
    pass

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
    mask = random.randint(2, size=P1.size)
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
    csp = CrewSchedulingProblem(open(args[0]))
    rotations = list(csp.generate_rotations())

if __name__ == '__main__':
    main()

