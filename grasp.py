#!/usr/bin/env python

from csp import CrewSchedulingProblem
from random import choice, random
from functools import partial
from sys import stdout
range = xrange

def DEBUG(s): print s

def DEBUG_RCL(rotations, rcl, selected_rotation,
              min_cost, max_cost, greedy_cost, stream=stdout):
    data = (len(rotations), len(rcl), min_cost, max_cost)
    def r_repr(r):
        s = '%s:%d:%d' % (str(r.tasks), r.cost, greedy_cost(r))
        bold = 1 if r == selected_rotation else 0
        color = 31 if greedy_cost(r) == max_cost else None
        if r in rcl:
            color = 32 if greedy_cost(r) == min_cost else 36
        if color:
            return '\033[%d;40;%dm%s\033[0m' % (bold, color, s)
        return s
    stream.write('#rotations: %d, #rcl: %d, cost range: [%d, %d]\n' % data)
    stream.write(' '.join(r_repr(r) for r in rotations))
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
    rotations = sorted(rotations, key=greedy_cost)
    solution = []
    while True:
        min_cost = greedy_cost(rotations[0])
        max_cost = greedy_cost(rotations[-1])
        threshold = min_cost + alpha * (max_cost - min_cost)
        rcl = [r for r in rotations if greedy_cost(r) <= threshold]
        selected_rotation = choice(rcl)
        solution.append(selected_rotation)

        DEBUG_RCL(rotations, rcl, selected_rotation, min_cost, max_cost, greedy_cost)

        # reevaluate candidates
        rotations = [r for r in rotations
                     if not (r.tasks & selected_rotation.tasks)]
        if sum(len(r.tasks) for r in solution) == len(csp.tasks):
            DEBUG_SOLUTION(solution)
            break
        elif not rotations:
            DEBUG('NOT A FEASIBLE SOLUTION')
            return None
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
    (options, args) = parser.parse_args()
    if not args:
        args = ['orlib/csp50.txt']

    csp = CrewSchedulingProblem(open(args[0]))
    rotations = list(csp.generate_rotations())

    greedy_cost = partial(rotation_cost, per_task_bonification=options.ptb, perturbation_radius=options.pertr)
    solution = grasp(rotations, csp, options.alpha, greedy_cost)

if __name__ == '__main__':
    main()

