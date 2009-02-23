#!/usr/bin/env python

# Genetic algorithm taken from:
#     P.C.Chu, J.E.Beasley.
#     Constraint Handling in Genetic Algorithms: The Set Partitioning Problem.
#     Journal of Heuristics, 11: 323--357 (1998)

from csp import CrewSchedulingProblem, namedtuple
from random import choice, randrange
from numpy import dot, zeros, array, matrix, random, sum, abs, transpose
from operator import attrgetter
from itertools import izip as zip
range = xrange

class Problem:
    # fields: A, c
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
        self.costs = array(costs)
        self.nr_tasks, self.nr_rotations = m, n
        self.alpha = map(frozenset, alpha)
        self.beta  = map(frozenset, beta)

    def __repr__(self):
        return '<CSP problem, %dx%d>' % (self.nr_tasks, self.nr_rotations)



Solution = namedtuple('Solution', 'columns covering fitness unfitness')

def make_solution(problem, columns):
    covering = dot(problem.A, columns)
    fitness = dot(problem.costs, columns)
    unfitness = sum(abs(covering - 1))
    return Solution(columns, covering, fitness, unfitness)

def initial_solution(problem):
    columns = zeros(problem.nr_rotations, dtype='uint8')
    I = frozenset(range(problem.nr_tasks))
    S, U = set(), set(I)
    while U:
        i = choice(list(U))
        J = [j for j in problem.alpha[i] if not (problem.beta[j] & (I - U))]
        if J:
            j = choice(J)
            columns[j] = 1
            U -= problem.beta[j]
        else:
            U.remove(i)
    #columns = random.randint(2, size=problem.nr_rotations).astype('uint8')
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

def static_mutation_bits(columns, M_s=3):
    bits = set()
    while len(bits) < M_s:
        bits.add(randrange(columns.size))
    return bits

def adaptive_mutation_bits(columns, M_a=5, epsilon=0.5):
    return set()


def repair(solution):
    # ...
    return solution
    
def ranking_replacement(population, child):
    # Labels for solutions according to relation with child.
    # Keys are pairs: (better fitness than child?, better unfitness than child?)
    groups = {
        (False, False): 1, (True, False): 2,
        (False, True):  3, (True, True):  4,
    }
    solution_group = (groups[solution.fitness   < child.fitness,
                             solution.unfitness < child.unfitness]
                      for solution in population)

    # replacement criteria:
    # 1. group with smallest label
    # 2. worst unfitness
    # 3. worst fitness
    sort_key = lambda (k, (sol, group)): (group, -sol.unfitness, -sol.fitness)
    worst_k, (worst_sol, worst_group) = min(
        ((k, (sol, group)) for k, (sol, group) in enumerate(zip(population, solution_group))),
        key=sort_key)

    population[worst_k] = child
    return worst_k



def best_solution(population):
    sort_key = lambda (k, sol): (sol.unfitness, sol.fitness)
    best_k, best_sol = min(((k, sol) for k, sol in enumerate(population)),
        key=sort_key)
    return best_k
    

def ga(problem, population_size=100, nr_iterations=1000):
    population = [initial_solution(problem) for k in range(population_size)]
    best_k = best_solution(population)
    for t in range(nr_iterations):
        p1, p2 = matching_selection(problem, population)
        child_columns = uniform_crossover(population[p1], population[p2])

        bits_to_mutate = static_mutation_bits(child_columns)
        for bit in bits_to_mutate:
            child_columns[bit] = 1 - child_columns[bit]

        bits_to_mutate = adaptive_mutation_bits(child_columns)
        for bit in bits_to_mutate:
            child_columns[bit] = 1 - child_columns[bit]

        child_columns = repair(child_columns)
        child = make_solution(problem, child_columns)
        child_k = ranking_replacement(population, child)
        if best_solution([population[best_k], child]) == 1:
            best_k = child_k
            print "Found better child!"
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

