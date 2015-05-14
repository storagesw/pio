import os
import copy

import config as cfg

class RunResults(object):
    """ Parsed results from a single PIO run """

    bw_dict = dict((bs, 0) for bs in cfg.BS_LIST)

    def __init__(self, pio_file):
        self.name = os.path.basename(pio_file)
        self.results = {
                'r': {'r': copy.deepcopy(self.bw_dict), # rand read
                      'w': copy.deepcopy(self.bw_dict)}, # rand write
                's': {'r': copy.deepcopy(self.bw_dict), # seq read
                      'w': copy.deepcopy(self.bw_dict)}} # seq write
        self.n_nodes = 0
        self.n_streams = 0
        print("Parsing {n}...".format(n=self.name))
        self.parse_out_file(pio_file)

    def parse_out_file(self, filepath):
        with open(filepath) as f:
            f.next() # 1st line is header
            nodes = set()
            tests = set()
            l_cnt = 0
            for line in f:
                l = line.split()
                self.results[l[0]][l[1]][l[2].lower()] += float(l[4])
                nodes.add(l[3])
                tests.add(str((l[0], l[1], l[2])))
                l_cnt += 1
        self.n_nodes = len(nodes)
        self.n_streams = l_cnt / len(tests)
                     
def list_files(path):
    files = []
    if os.path.isdir(path):
        for f in os.listdir(path):
            f_path = path + '/' + f
            if is_pio_file(f_path):
                files.append(f_path)
    else: # raise some exception?
        print('{p} not a directory!'.format(p=path))
        exit()
    return files

def is_pio_file(f):
    return os.path.isfile(f) and f.endswith(cfg.FILE_EXT)

def extract_data(files):
    parsed = []
    for f in files:
        parsed.append(RunResults(f))
    return parsed

def generate_gp(rr_list, args):
    with open(cfg.PLOT_FNAME, 'w') as p:
        p.write(
"""\
reset
set terminal png nocrop noenhanced font arial 11
set xlabel 'Block Size'
set xtics ('{0}' 0, '{1}' 1, '{2}' 2, '{3}' 3, '{4}' 4)
set ylabel 'MB/s'
set xtics nomirror
set datafile missing '?'
set offset graph 0.1, graph 0.1, graph 0.1, graph 0
set grid ytics\n
""".format(*(cfg.BS_LIST)))
        for o, d in [('r', 'r'), ('r', 'w'), ('s', 'r'), ('s', 'w')]:
            p.write("set title '{t}' font \"arial,14\"\n"
                    "set output '{t}.png'\n"
                    "plot ".format(t=expand(o, d)))
            for rr in rr_list:
                if args.aggr:
                    p.write("'-' using 0:($1/1024) with linespoints title "
                            "'{name}', ".format(name=rr.name))
                if args.node_avg:
                    p.write("'-' using 0:($1/1024) with linespoints title "
                            "'{name}_node_avg', ".format(name=rr.name))
                if args.stream_avg:
                    p.write("'-' using 0:($1/1024) with linespoints title "
                            "'{name}_stream_avg', ".format(name=rr.name))
            p.write("\n")
            for rr in rr_list:
                if args.aggr:
                    for bs in cfg.BS_LIST:
                        p.write(str(rr.results[o][d][bs]) + "\n")
                    p.write("e\n")
                if args.node_avg:
                    for bs in cfg.BS_LIST:
                        p.write(str(rr.results[o][d][bs]/rr.n_nodes) + "\n")
                    p.write("e\n")
                if args.stream_avg:
                    for bs in cfg.BS_LIST:
                        p.write(str(rr.results[o][d][bs]/rr.n_streams) + "\n")
                    p.write("e\n")

def expand(order, direction):
    s = ""
    if order == 'r':
        s += 'random_'
    else:
        s += 'sequential_'
    if direction == 'r':
        s += 'read'
    else:
        s += 'write'
    return s
