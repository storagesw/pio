import os
import subprocess

import config as cfg

def init(path):
    df, cf = full(path)
    with open(df, 'w') as f:
        f.write(os.urandom(cfg.DUR_SIZE))
    with open(cf, 'w') as f:
        cmd = 'sha1sum {df}'.format(df=df)
        f.write(run(cmd))
    validate(path)
    print 'Initialization successful'

def validate(path):
    cf = full(path)[1]
    cmd = 'sha1sum -c {cf}'.format(cf=cf)
    if 'FAILED' in run(cmd):
        print 'Validation fail!'
    else:
        print '{cf} is valid!'.format(cf=cf)

def run(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            shell=True).communicate()[0]

def full(path):
    return [path + '/' + f for f in cfg.DUR_FILE, cfg.CHK_FILE]
