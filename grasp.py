#!/usr/bin/env python

from csp import CrewSchedulingProblem
from random import choice, random
from functools import partial
range = xrange

def DEBUG(s): print s

def rotation_cost(r, per_task_bonification=0, perturbation_radius=0):
    """Cost of adding a rotation to a solution"""
    return (-per_task_bonification * len(r.tasks) +
             perturbation_radius * random() +
             r.cost)

def construct_solution(rotations, csp, greedy_cost):
    rotations = rotations[:]
    solution = []
    while True:
        rcl = sorted(rotations, key=greedy_cost)[:10]
        selected_rotation = choice(rcl)
        DEBUG('Selection from RCL: %s' % str(selected_rotation))
        solution.append(selected_rotation)

        # reevaluate candidates
        rotations = [r for r in rotations
                     if not (r.tasks & selected_rotation.tasks)]
        DEBUG('%d candidates remaining' % len(rotations))
        if sum(map(len, [r.tasks for r in solution])) == len(csp.tasks):
            DEBUG('SOLUTION WITH %d ROTATIONS:' % len(solution))
            for r in solution: print r.tasks,
            print
            break
        if not rotations:
            DEBUG('NOT A FEASIBLE SOLUTION')
            break
    return solution

def local_search(solution):
    return solution

def grasp(rotations, csp, max_iterations=1):
    greedy_cost = partial(rotation_cost,
                          per_task_bonification=300, perturbation_radius=0)
    best_solution = None
    for i in range(max_iterations):
        solution = construct_solution(rotations, csp, greedy_cost)
        solution = local_search(solution)
        best_solution = solution
        break
    return best_solution

def main():
    import sys
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'orlib/csp50.txt'
    csp = CrewSchedulingProblem(open(filename))
    rotations = list(csp.generate_rotations())
    solution = grasp(rotations, csp)

if __name__ == '__main__':
    main()

