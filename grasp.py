#!/usr/bin/env python

from csp import CrewSchedulingProblem, namedtuple
from random import choice, random
from functools import partial
from operator import attrgetter
from sys import stdout
range = xrange

Candidate = namedtuple('Candidate', 'rotation, greedy_cost')

def DEBUG_RCL(candidates, rcl, selected_candidate, stream=stdout):
    min_cost = candidates[0].greedy_cost
    max_cost = candidates[-1].greedy_cost
    def c_repr(c):
        r = c.rotation
        s = '%s:%d:%d' % (str(r.tasks), r.cost, c.greedy_cost)
        bold = 1 if c == selected_candidate else 0
        color = 31 if c.greedy_cost == max_cost else None
        if c in rcl:
            color = 32 if c.greedy_cost == min_cost else 36
        if color:
            return '\033[%d;49;%dm%s\033[0m' % (bold, color, s)
        return s
    data = (len(candidates), len(rcl), min_cost, max_cost)
    stream.write('#candidate rotations: %d, #rcl: %d, cost range: [%d, %d]\n' % data)
    stream.write(' '.join(c_repr(c) for c in candidates))
    stream.write('\n')

def DEBUG_SOLUTION(rotations, stream=stdout):
    cost = sum(r.cost for r in rotations)
    nr_rotations = len(rotations)
    stream.write('SOLUTION FOUND cost:%d, nr_rotations: %d\n' %
            (cost, nr_rotations))
    stream.write(' '.join(str(r.tasks) for r in rotations))
    stream.write('\n')
    


def rotation_cost(r, per_task_bonification=0, perturbation_radius=0):
    """Cost of adding a rotation to a solution"""
    return (-per_task_bonification * len(r.tasks) +
             perturbation_radius * random() +
             r.cost)

def construct_solution(rotations, csp, greedy_cost, alpha):
    candidates = sorted((Candidate(r, greedy_cost(r)) for r in rotations),
                        key=attrgetter('greedy_cost'))
    solution = []
    while sum(len(r.tasks) for r in solution) < len(csp.tasks):
        if not candidates:
            return None

        min_cost = candidates[0].greedy_cost
        max_cost = candidates[-1].greedy_cost
        threshold = min_cost + alpha * (max_cost - min_cost)
        rcl = [c for c in candidates if c.greedy_cost <= threshold]
        selected_candidate = choice(rcl)
        solution.append(selected_candidate.rotation)

        DEBUG_RCL(candidates, rcl, selected_candidate)

        # reevaluate candidates
        candidates = [c for c in candidates
                      if not (c.rotation.tasks & selected_candidate.rotation.tasks)]
    DEBUG_SOLUTION(solution)
    return solution

def local_search(solution):
    return solution

def grasp(rotations, csp, alpha, greedy_cost, max_iterations=1):
    best_solution = None
    for i in range(max_iterations):
        solution = construct_solution(rotations, csp, greedy_cost, alpha)
        solution = local_search(solution)
        best_solution = solution
        break
    return best_solution

def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] [input_file]")
    parser.add_option('-a', '--alpha', type='float', default=0.3, metavar='NUM', help='Alpha parameter for RCL construction')
    parser.add_option('-b', '--ptb',   type='float', default=300, metavar='NUM', help='Per task bonification in greedy function')
    parser.add_option('-p', '--pertr', type='float', default=0,   metavar='NUM', help='Cost perturbation radius in greedy function')
    parser.add_option('--debug-greedy', action='store_true', help='Print debugging data for construction stage')
    parser.add_option('--debug-search', action='store_true', help='Print debugging data for search stage')
    (options, args) = parser.parse_args()
    if not args:
        args = ['orlib/csp50.txt']

    if not options.debug_greedy:
        global DEBUG_SOLUTION, DEBUG_RCL
        DEBUG_SOLUTION = lambda *args: None
        DEBUG_RCL = lambda *args: None

    csp = CrewSchedulingProblem(open(args[0]))
    rotations = list(csp.generate_rotations())

    greedy_cost = partial(rotation_cost, per_task_bonification=options.ptb, perturbation_radius=options.pertr)
    solution = grasp(rotations, csp, options.alpha, greedy_cost)

if __name__ == '__main__':
    main()

