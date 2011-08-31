"""Setup file for packaging swigibpy"""

from distutils.core import setup, Extension

IB_DIR = 'IB_965'
VERSION = '0.2'

ib_module = Extension('_swigibpy',
                      sources=[IB_DIR + 
                               '/PosixSocketClient/EClientSocketBase.cpp',
                               IB_DIR + 
                               '/PosixSocketClient/EPosixClientSocket.cpp',
                               IB_DIR + '/swig_wrap.cpp'],
                      include_dirs=[IB_DIR,
                                    IB_DIR + '/PosixSocketClient',
                                    IB_DIR + '/Shared'],
                      define_macros=[ ('IB_USE_STD_STRING', '1') ]
                      )

setup (version=VERSION,
       name='swigibpy',
       author="komnomnomnom",
       description="""SWIG Python wrapper for Interactive Brokers C++ API""",
       ext_modules=[ib_module],
       py_modules=["swigibpy"],
       )
