import argparse

import perf
import dur
import plot
import config as cfg

def main():
    r = parse_args()
    cfg.DEBUG = r.debug
    if r.sub == 'perf':
        cmd_perf(r)
    elif r.sub == 'dur':
        cmd_dur(r)
    elif r.sub == 'plot':
        cmd_plot(r)

def cmd_perf(r):
    limit = perf.lim(r.test_list[0], r.driver, r.limit)
    ts = perf.TestSuite(r.driver, limit, r.streams, r.nodes_paths,
        r.test_list[1])
    ts.run_tests()
    with open(r.out + '.pio', 'w') as f:
        ts.write_report(f)

def cmd_dur(r):
    if r.cmd == 'init':
        dur.init(r.path)
    elif r.cmd == 'validate':
        dur.validate(r.path)

def cmd_plot(r):
    files = plot.list_files(r.path)
    data = plot.extract_data(files)
    plot.generate_gp(data, r)
    print("Now you can run: 'gnuplot plot.gp'")

def parse_args():
    parser = argparse.ArgumentParser(description='Parallel IO benchmarking')
    subparsers = parser.add_subparsers(dest='sub')
    parser.add_argument('-D', '--debug', action='store_true',
            help='Be very verbose.')

    p_run = subparsers.add_parser('perf')
    a = p_run.add_argument
    a('-t', dest='test_list', type=perf.parse_tests, default='full',
        help="'full' for a complete benchmark, 'quick' for a quick one, "
             "and 'random,sequential:read,write:{0}' (it's possible to "
             "remove some options) for a custom test.".format(
            ','.join(cfg.BS_LIST)))
    a('driver', choices=['fio', 'fstest'],
      help='Benchmark using fio or fstest')
    a('-o', dest='out', default='/dev/stdout', 
        help='Path to output file. Default: stdout')
    a('-l', dest='limit', help='Test limit as defined by the driver')
    a('-s', dest='streams', type=int, default=1, 
        help="Number of streams on each node")
#    a('path', help='Mount point of examined filesystem')
    a('nodes_paths', nargs='+', 
        help='Addresses of the target nodes alongside paths to run IO against '
             'in each node. Space-separated list of values of the format '
             '\'node01,node02,..,nodeXX:/path/to/dir1,..,/path_to/dirX\'')

    p_plot = subparsers.add_parser('plot')
    a = p_plot.add_argument 
    a('-a', '--aggr', action='store_true',
            help='Add total aggregated result')
    a('-n', '--node_avg', action='store_true',
            help='Add per node average to plot')
    a('-s', '--stream_avg', action='store_true',
            help='Add per stream average to plot')
#    a('-d', '--data_kpi', action='store_true',
#            help='Add HANA data volume KPI to plot')
#    a('-l', '--log_kpi', action='store_true',
#            help='Add HANA log volume KPI to plot')
    a('path', help='Paths to directory to plot')

    p_dur = subparsers.add_parser('dur')
    a = p_dur.add_argument
    a('cmd', choices=['init', 'validate'])
    a('path', help="Path to lay file")
    
    return parser.parse_args() 

if __name__ == '__main__':
    main()

