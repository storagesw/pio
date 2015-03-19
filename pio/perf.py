from ClusterShell.Task import task_self
import argparse

import drivers
import config as cfg

class Test(object):
    def __init__(self, order, direction, blocksize):
        self.o = order
        self.bs = blocksize
        self.d = direction
        self.results = []

class TestSuite(object):
    def __init__(self, driver, path, limit, nodes, streams, tests):
        try:
            self.driver = getattr(drivers, driver)
        except AttributeError:
            raise argparse.ArgumentTypeError("Driver not found.")
        self.path = path
        self.limit = limit
        self.nodes = nodes
        self.streams = streams
        self.tests = tests

    def run_tests(self):
        for t in self.tests:
            print('Running {0} {1} {2}...'.format(t.o, t.bs, t.d))
            self.run_test(t)
            self.update_test_results(t)

    def run_test(self, test):
        for i in range(self.streams):
            cmd = self.driver.gen_cmd(test, i, self.limit, self.path)
            cfg.dprint("Listing: " + cmd)
            task.shell(cmd, nodes=','.join(self.nodes)) 
        cfg.dprint("Running above commands.")
        task.resume()

    def update_test_results(self, test):
        for buf, nodes in task.iter_buffers():
            test_out = str(buf)
            cfg.dprint(test_out)
            bw = self.driver.parse_bw(test_out)
            test.results += [(n, bw) for n in nodes]

    def write_report(self, f):
        f.write('ORDER DIRECTION BS_KB/s NODE BW\n')
        for t in self.tests:
            for n, bw in t.results: 
                f.write('{o} {d} {bs:<4} {n:<10} {bw}\n'.format(o=t.o[0],
                    d=t.d[0], bs=t.bs, n=n, bw=bw))

def parse_tests(tests):
    directions = ['read', 'write']
    if tests == 'full':
        return 'f', [Test(o, d, bs) for o in ['random', 'sequential']
                                    for d in directions
                                    for bs in cfg.BS_LIST]
    elif tests == 'quick':
        return 'q', ([Test('random', d, '4k') for d in directions] +
                     [Test('sequential', d, '1M') for d in directions])
    else:
        try:
            params = tests.split(':')
            orders = params[0].split(',')
            directions = params[1].split(',')
            block_sizes = params[2].split(',')
            return '', [Test(o, d, bs) for o in orders
                                       for d in directions
                                       for bs in block_sizes]
        except Exception: # Which exact exception?
            msg = ("test must be either 'full', 'quick', or of the form "
                   "'random,sequential:read,write:{0}', where at least 1 "
                   "argument should be specified between each colon.".format(
                       ','.join(cfg.BS_LIST)))
            raise argparse.ArgumentTypeError(msg)

def lim(indicator, driver, limit):
    if limit is not None:
        return limit
    lim_dict = {'f': {'fio': 60, 'fstest': '1G'},
                'q': {'fio': 6, 'fstest': '64M'},
                '': {'fio': 60, 'fstest': '1G'}}
    return lim_dict[indicator][driver]

task = task_self()
