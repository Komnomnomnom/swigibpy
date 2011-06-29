#!/usr/bin/env python

"""
setup file for building and installing Interactive Brokers SWIG wrapper
 
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
