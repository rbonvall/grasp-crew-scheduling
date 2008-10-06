#!/usr/bin/env python

from collections import defaultdict
range = xrange
try:
    from collections import namedtuple
except ImportError:
    from namedtuple import namedtuple

Task = namedtuple('Task', ['start', 'finish'])

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
            if finish_time - start_time > self.time_limit:
                continue
            
            yield rotation
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

    # test generation of rotations
    data = []
    for n, rotation in enumerate(csp.generate_rotations()):
        cost = sum(csp.transition_costs[t] for t in zip(rotation, rotation[1:]))
        start_time, _  = csp.tasks[rotation[0]]
        _, finish_time = csp.tasks[rotation[-1]]
        duration = finish_time - start_time
        r = str(tuple(x+1 for x in rotation))
        data.append((r, cost, duration))

    try:
        from ptable import Table
    except ImportError:
        pass
    else:
        t = Table(data)
        t.headers = ('Rotation', 'Cost', 'Duration')
        t.align = 'lrr'
        t.col_separator = ' | '
        t.repeat_headers_after = 25
        t.header_separator = True
        t.print_table()
    print '# of rotations: %d' % (n + 1)

if __name__ == '__main__':
    main()

