#!/usr/bin/env python

"""
setup.py file for building Interactive Brokers SWIG wrapper

To build execute the following commands from the root of the 
interactive brokers API directory:

 - (optional, swig 2.0+ required) swig -c++ -python -o swig_wrap.cpp -outdir .. ../swigify_ib.i
 - python ../ib_build.py build_ext --build-lib ..
 
 @author: Kieran O'Mahony
"""

from distutils.core import setup, Extension

ib_module = Extension('_ib',
                      sources=['PosixSocketClient/EClientSocketBase.cpp', 
                               'PosixSocketClient/EPosixClientSocket.cpp',
                               'swig_wrap.cpp'],
                      include_dirs=['.',
                                    'PosixSocketClient',
                                    'Shared'],
                      define_macros=[ ('IB_USE_STD_STRING','1') ]
                      )

setup (name = 'IB API',
       version = '9.64',
       author      = "Interactive Brokers",
       description = """SWIG wrapper generation for Interactive Brokers C++ API""",
       ext_modules = [ib_module],
       py_modules = ["ib"],
       )