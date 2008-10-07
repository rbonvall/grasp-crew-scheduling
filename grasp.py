#!/usr/bin/env python

from csp import CrewSchedulingProblem
range = xrange

def construct_solution(rotations, csp):
    pass

def local_search(solution):
    return solution

def grasp(rotations, csp, max_iterations=1):
    best_solution = None
    for i in range(max_iterations):
        solution = construct_solution(rotations, csp)
        solution = local_search(solution)
        best_solution = solution
        break
    return best_solution

def main():
    filename = "orlib/csp50.txt"
    csp = CrewSchedulingProblem(open(filename))
    rotations = list(csp.generate_rotations())
    solution = grasp(rotations, csp)

if __name__ == '__main__':
    main()

