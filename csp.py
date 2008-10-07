#!/usr/bin/env python

from collections import defaultdict
from itertools import izip as zip
range = xrange
try:
    from collections import namedtuple
except ImportError:
    from namedtuple import namedtuple

Task = namedtuple('Task', ['start', 'finish'])
Rotation = namedtuple('Rotation', ['tasks', 'cost', 'duration'])

class CrewSchedulingProblem:
    """Crew Scheduling problem instance from ORLIB."""
    def __init__(self, input_file):
        file_contents = [tuple(map(int, line.split())) for line in input_file]
        nr_tasks, time_limit = file_contents.pop(0)

        self.time_limit = time_limit
        self.tasks = [Task(*t) for t in file_contents[:nr_tasks]]
        self.transition_costs = defaultdict(lambda: float('inf'))
        self.possible_transitions = [list() for task in self.tasks]
        for i, j, cost in file_contents[nr_tasks:]:
            # Reindex to start from 0, not from 1 as in ORLIB instances
            self.transition_costs[i - 1, j - 1] = cost
            self.possible_transitions[i - 1].append(j - 1)

    def generate_rotations(self, from_rotation=()):
        if from_rotation:
            candidates = self.possible_transitions[from_rotation[-1]]
        else:
            candidates = range(len(self.tasks))

        for task in candidates:
            rotation = from_rotation + (task,)
            start_time  = self.tasks[rotation[0]].start
            finish_time = self.tasks[rotation[-1]].finish
            duration = finish_time - start_time
            if duration > self.time_limit:
                continue
            cost = sum(self.transition_costs[t] for t in zip(rotation, rotation[1:]))
            yield Rotation(set(rotation), cost, duration)

            for r in self.generate_rotations(rotation):
                yield r



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
    print

    try:
        from ptable import Table
    except ImportError:
        pass
    else:
        t = Table(csp.generate_rotations())
        t.headers = ('Rotation', 'Cost', 'Duration')
        t.align = 'lrr'
        t.col_separator = ' | '
        t.repeat_headers_after = 25
        t.header_separator = True
        t.print_table()
    print '# of rotations: %d' % (len(t.data))

if __name__ == '__main__':
    main()

