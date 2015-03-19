import json

def gen_cmd(test, stream_num, limit, path):
    """ generate a command to run from shell and print the results """
    cmd = (
        'LD_LIBRARY_PATH={lib_path} {lib_path}/fstest '
        '{d} ' # direction {read,write}
        '--total {fsize} '
        '--block {bs} '
        '--{o} ' # order {random, sequential}
        '--json ' 
        '--path {p}/`hostname`_{s}').format(lib_path=LIB_PATH, d=test.d, 
                fsize=limit, bs=test.bs, o=test.o, p=path, s=stream_num)
    return cmd

def parse_bw(test_out):
    """ returns the bw from cmd's output """
    if 'Read' in test_out: # fixing fstest unvalidated json
        test_out = test_out[:-4] + '}'

    dic = json.loads(test_out)
    if 'Read' in dic.keys():
        bw = int(float(dic['Read'][0]['IoThroughput']))*1024
    elif 'Overwrite' in dic.keys():
        bw = int(float(dic['Overwrite'][1]['IoThroughput']))*1024
    return bw

def validate_limit(limit):
    """ validates the given limit to work with the driver """
    # need to implement
    pass

def init_env():
    """ return initialization command to run before all the tests """
    return "; ".join(["mkdir -p {path}/\${{HOSTNAME}}_{s}".format(path=path,
                     s=s) for s in range(streams)])
