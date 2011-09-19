"""Setup file for packaging swigibpy"""

import os
from distutils.core import setup, Extension

###

IB_DIR = 'IB_965'
VERSION = '0.2.1'

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
       author="Kieran O'Mahony",
       author_email="kieranom@gmail.com",
       url = "http://komnomnomnom.github.com/swigibpy/",
       license = 'New BSD License',
       description="""Third party Python API for Interactive Brokers""",
       long_description=file(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
       keywords = ["interactive brokers", "tws"],
       ext_modules=[ib_module],
       py_modules=["swigibpy"],
       classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Development Status :: 4 - Beta",
            "Environment :: Other Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Office/Business :: Financial",
            ],
       )
