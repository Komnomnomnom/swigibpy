"""Setup file for packaging swigibpy"""

from distutils.core import setup, Extension

###

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
       author="Kieran O'Mahony",
       author_email="kieranom@gmail.com",
       url = "http://komnomnomnom.github.com/swigibpy/",
       license = 'New BSD License',
       description="""Third party Python API for Interactive Brokers""",
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
       
       # Auto generate reStructuredText from markdown README.md using pandoc
       # http://johnmacfarlane.net/pandoc/try
       long_description="""\
Overview
========

`Interactive Brokers`_ Python API, auto generated from C++ API using
`SWIG`_.

Latest version: 0.2 (TWS API v9.65)

Install
=======

Use pip (recommended)

::

    $ pip install swigibpy

Alternatively download your archive of choice and run

::

    $ python setup.py install

Usage
=====

To use simply import the swigibpy module, see the examples directory for
more. For API reference refer to the `C++ API documentation`_.

Develop
=======

Contributions are welcome! For developement you can build the extension
in the current dir

::

    $ python setup.py build_ext --build-lib .

To regenerate the SWIG wrappers (SWIG 2.0+ required), in the IB API
directory run:

::

    $ swig -v -c++ -python -threads -o swig_wrap.cpp -outdir .. -modern 
        -fastdispatch -nosafecstrings -noproxydel -fastproxy -fastinit 
        -fastunpack -fastquery -modernargs -nobuildnone ../swigify_ib.i

**NOTE:** SWIG options -builtin and -fvirtual are not compatible with
swigibpy's interface file.

License
=======

swigibpy original code is free software under the New BSD license.

Interactive Brokers propriety C++ API is copyright Interactive Brokers
LLC. swigibpy is in no way supported or endorsed by Interactive Brokers
LLC.

--------------

.. _Interactive Brokers: http://www.interactivebrokers.co.uk/
.. _SWIG: http://www.swig.org/
.. _C++ API documentation: http://www.interactivebrokers.com/en/p.php?f=programInterface
""",
       )
