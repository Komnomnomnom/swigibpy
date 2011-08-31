"""Setup file for packaging swigibpy"""

from distutils.core import setup, Extension
import os

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
       url = "http://komnomnomnom.github.com/swigibpy/",
       description="""Third party Python API for Interactive Brokers""",
       long_description=file(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
       keywords = ["interactive brokers", "tws"],
       ext_modules=[ib_module],
       py_modules=["swigibpy"],
       )
