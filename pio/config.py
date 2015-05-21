LIB_PATH = "lib"

README_FILE = "README"
BS_LIST = ["4k", "16k", "64k", "256k", "1m"]

FILE_EXT = (".pio")
PLOT_FNAME = "plot.gp"

DUR_FILE = "dur_file"
CHK_FILE = "chk_file"
DUR_SIZE = 1*1024*1024*1024 # 1GB

DEBUG = False

# Max jobs that can run simultaneously
SSH_FANOUT = 512 

def dprint(s):
    if DEBUG:
        print s
