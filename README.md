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

- Setup no password SSH between participating hosts

- Install FIO

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
    libhdbbasis.so, libhdblttbase.so, libhdbversion.so

- Install PIO: 

        python setup.py install

Perf
----
    pio perf -h

Plot
----
    pio plot -h

Durability
----------
    pio dur -h


Development Mode
----------------
    python setup.py develop

Contact
-------
Irad Cohen, irad.cohen@sap.com
Aidan Shribman, aidan.shribman@sap.com
Mark Kemel, mark.kemel@sap.com
