PIO - Parallel IO
=================

A framework for synchronized, concurrent, high-performance IO evaluation.

Setup
-----
- Ensure you have Python 2.6 or 2.7 installed

        python --version

- Install Python setuptools

        # check if setuptools are installed
        python -c 'import setuptools'

        # if not then
        wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py	
        python ez_setup.py --insecure

- Setup no password SSH to all slave nodes (in this example they are named 
  node01, node02 and node03):

        ssh-keygen -t rsa -N ''
		for n in node01 node02 node03; do
			ssh-copy-id -i ~/.ssh/id_rsa.pub $n
		done

- Install PIO (master node only): 

        python setup.py install

- Install FIO on all slave nodes:

        # setup libAIO
        zypper install libaio libaio-devel          # sles
        yum install libaio libaio-devel             # redhat
        apt-get install libaio libaio-devel         # debian, ubuntu

        # install latest FIO version
        git clone http://git.kernel.dk/fio.git
        cd fio
        ./configure
        make
        make install

- *OPTIONAL* Installing FSTEST - contact SAP for the following files: fstest, 
    libhdbbasis.so, libhdblttbase.so, libhdbversion.so and run:
        mkdir -p lib/fstest
		cp fstest lib/fstest/
		cp libhdb*.so lib/fstest/


Usage
-----
#### Performance Scenario
For example, a master node coordinates 3 slave nodes (node01, node02 and 
node03) to run several fio workloads that cover reads and writes, with 
different block sizes (4k, 16k, 64k, 256k, 1M), all random, where each job is 
run for 60 seconds.

    pio perf -t random:read,write:4k,16k,64k,256k,1M -o output_file -l 60 \
	    fio /mnt/storage node01 node02 node03

- "/mnt/storage" is a directory that is accessible on all slave nodes (does not
   have to be shared).


In order to plot the data to a nice graph, run:

    pio plot -a .
	gnuplot plot.gp

#### Durability Scenario
Initialize a data file that lays on the evaluated storage system. Mess around
with the system (power shortage, faulty disks, etc.), then check that the data
is not corrupted.

    pio dur init /mnt/storage

    pio dur validate /mnt/storage

