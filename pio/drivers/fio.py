import re

def gen_cmd(test, stream_num, limit, path):
    """ generate a command to run from shell and print the results """
    cmd = ('fio --name=`hostname`_{s} '
        '--rw={rw} '
        '--bs={bs} '
        '--ramp_time={ramp_time} '
        '--runtime={runtime} '
        '--overwrite=1 '
        '--randrepeat=0 ' 
        '--ioengine=libaio '
        '--iodepth=256 '
        '--direct=1 ' 
        '--time_based '
        '--refill_buffers '
        '--filesize=1G '
        '--directory={path}'.format(s=stream_num, rw=test.d, bs=test.bs, 
            ramp_time=int(limit)/3, runtime=int(limit)*2/3, path=path))
    return cmd

def to_kbps(s):
    if s.endswith('MB/s'):
        return float(s[:-4])*1024
    elif s.endswith('KB/s'):
        return float(s[:-4])
    elif s.endswith('B/s'):
        return float(s[:-3])//1024
    else:
        raise Exception # which exception?

bw_re = re.compile('bw=(.*?),')

def parse_bw(test_out):
    """ returns the bw from cmd's output """
    found = bw_re.search(test_out)
    assert found != None
    return to_kbps(found.group(1))

def validate_limit(limit):
    """ validates the given limit to work with the driver """
    try:
        int(limit)
    except ValueError:
        msg = "fio limit must be a number of seconds."
        raise argparse.ArgumentTypeError(msg)
