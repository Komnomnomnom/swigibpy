Overview
========

Interactive Brokers (IB) Python API, auto generated from IB C++ API using SWIG.
Supports IB API version 9.64

Install
=======

To build and install as a Python extension (recommended):

    $ sudo python setup.py install
    
Usage
=====

To use simply import the swigibpy module, see the examples directory for more.

Develop
=======
    
For developement you can build the extension in the current dir 

    $ python setup.py build_ext --build-lib .
 	
To regenerate the SWIG wrappers (SWIG 2.0+ required), in the IB API 
directory run:

    $ swig -v -c++ -python -threads -o swig_wrap.cpp -outdir .. -modern 
        -fastdispatch -nosafecstrings -noproxydel -fastproxy -fastinit 
        -fastunpack -fastquery -modernargs -nobuildnone ../swigify_ib.i
        
__NOTE:__ SWIG options -builtin and -fvirtual are not compatible with swigibpy's
interface file.

