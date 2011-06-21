#!/usr/bin/env python

"""
setup.py file for building and installing Interactive Brokers SWIG wrapper

To build and install the ib module:
    $ sudo python ib_build.py install

Optional:
swig 2.0+ is required for this step.
To build the swig libraries, in the IB API directory, run
    $ swig -c++ -python -o swig_wrap.cpp -outdir .. ../swigify_ib.i
 
 
 @author: Kieran O'Mahony
"""

from distutils.core import setup, Extension

IB_DIR = 'IB_964'

ib_module = Extension('_ib',
                      sources=[IB_DIR + 
                               '/PosixSocketClient/EClientSocketBase.cpp', 
                               IB_DIR + 
                               '/PosixSocketClient/EPosixClientSocket.cpp',
                               IB_DIR + '/swig_wrap.cpp'],
                      include_dirs=[IB_DIR,
                                    IB_DIR + '/PosixSocketClient',
                                    IB_DIR + '/Shared'],
                      define_macros=[ ('IB_USE_STD_STRING','1') ]
                      )

setup (name = 'IB API',
       version = '9.64',
       author      = "Interactive Brokers",
       description = """SWIG wrapper generation for Interactive Brokers C++ API""",
       ext_modules = [ib_module],
       py_modules = ["ib"],
       )
