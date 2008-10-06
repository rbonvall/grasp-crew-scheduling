#!/usr/bin/env python

from collections import defaultdict

class CrewSchedulingProblem:
    """Crew Scheduling problem instance from ORLIB."""
    def __init__(self, input_file):
        file_contents = [tuple(map(int, line.split())) for line in input_file]
        nr_tasks, time_limit = file_contents.pop(0)

        self.time_limit = time_limit
        self.tasks = file_contents[:nr_tasks]
        self.transition_costs = defaultdict(lambda: float('inf'))
        self.possible_transitions = [list() for task in self.tasks]
        for i, j, cost in file_contents[nr_tasks:]:
            # Reindex to start from 0, not from 1 as in ORLIB instances
            self.transition_costs[i - 1, j - 1] = cost
            self.possible_transitions[i - 1].append(j - 1)


def main():
    import sys

    if len(sys.argv) < 2 or sys.argv[1] == '-':
        problem_file = sys.stdin
    else:
        try:
            problem_file = open(sys.argv[1])
        except IOError:
            sys.stderr.write("Couldn't open file %s\n" % problem_file)
            sys.exit(-1)

    csp = CrewSchedulingProblem(problem_file)

    if problem_file == sys.stdin:
        print '--- Problem from stdin ---'
    else:
        print '--- Problem: %s ---' % (sys.argv[1])
    
    print 'Problem size: %d' % len(csp.tasks)
    print 'Time limit: %d  ' % csp.time_limit
    print 'Transitions: %d ' % len(csp.transition_costs)


if __name__ == '__main__':
    main()

