#!/usr/bin/env python

from csp import CrewSchedulingProblem
from random import choice, random
from functools import partial
range = xrange

def DEBUG(s): print s
def DEBUG_RCL(rotations, rcl, selected_rotation, min_cost, max_cost, greedy_cost):
    data = (len(rotations), len(rcl), min_cost, max_cost)
    DEBUG('#rotations: %d, #rcl: %d, min_cost: %d, max_cost: %d' % data)
    rotation_reprs = []
    for r in rotations:
        r_repr = '%s:%d' % (str(r.tasks), greedy_cost(r))
        if r in rcl:
            c = int(r == selected_rotation)
            if greedy_cost(r) == min_cost:
                r_repr = '\033[%d;40;32m%s\033[0m' % (c, r_repr)
            else:
                r_repr = '\033[%d;40;36m%s\033[0m' % (c, r_repr)
        if greedy_cost(r) == max_cost:
            r_repr = '\033[0;40;31m%s\033[0m' % r_repr
        rotation_reprs.append(r_repr)
    DEBUG(' '.join(rotation_reprs))


def rotation_cost(r, per_task_bonification=0, perturbation_radius=0):
    """Cost of adding a rotation to a solution"""
    return (-per_task_bonification * len(r.tasks) +
             perturbation_radius * random() +
             r.cost)

def construct_solution(rotations, csp, greedy_cost):
    rotations = rotations[:]
    solution = []
    alpha = 0.8
    while True:
        min_cost = greedy_cost(min(rotations, key=greedy_cost))
        max_cost = greedy_cost(max(rotations, key=greedy_cost))
        threshold = min_cost + alpha * (max_cost - min_cost)
        #rcl = sorted(rotations, key=greedy_cost)[:10]
        rcl = [r for r in rotations if greedy_cost(r) <= threshold]
        selected_rotation = choice(rcl)
        solution.append(selected_rotation)

        DEBUG_RCL(rotations, rcl, selected_rotation, min_cost, max_cost, greedy_cost)

        # reevaluate candidates
        rotations = [r for r in rotations
                     if not (r.tasks & selected_rotation.tasks)]
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

