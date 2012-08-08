Overview
========

`Interactive Brokers`_ Python API, auto generated from C++ API using `SWIG`_.

Latest version: 0.3 (TWS API v9.66)

Install
=======

Use pip (recommended)::

    $ pip install swigibpy

Alternatively download your archive of choice and run::

    $ python setup.py install

Notes for Windows Users
=======================

swigibpy just provides a wrapper around the TWS C++ API so this needs to be
compiled for your target platform during installation. While this should
'just work' for Linux and OSX, Windows users might need to do some extra work.

Compile with MinGW
------------------

Download and install `MinGW`_ and follow the steps to `add MinGW
to your path`_.  Note there is a `compatability problem`_ between the latest
version of MinGW and disutils so it is recommended to install an older version
until this is resolved (mingw-get-inst-20110802.exe has been known to work).

To get pip to use MinGW as the compiler edit or create a
file named ``distutils.cfg`` in ``[PYTHON LOCATION]\Lib\distutils`` where
``[PYTHON LOCATION]`` is the path to your Python install, e.g. ``C:\Python27``.
Add the following to ``distutils.cfg``::

	[build]
	compiler=mingw32

then use the pip command above and with a bit of luck, you're done!

Alternatively you can download and build the package directly. To build and
install use::

	$ python setup.py build -c mingw32
	$ python setup.py install

This has been verified to work using MinGW and Python 2.7 on Windows 7, Vista,
and XP.

Compile with Visual Studio
--------------------------

Several users have reported success building swigibpy with Visual Studio, with 
a few caveats:

- Distutils has issues building with anything later than Visual Studio 2008
  (version 9).
- The MFC library is required by the TWS API.
- Visual Studio 11 doesn't like the ``/MD`` compile flag, which distutils adds.
  For a workaround see `here`_.

Usage
=====

To use simply import the swigibpy module, see the examples directory for more.
For API reference refer to the `C++ API documentation`_.

swigibpy operates by periodically polling TWS for messages. The default poll 
interval is half a second but this can be customised by passing a 
``poll_interval`` argument to ``eConnect``::
    
    tws.eConnect("", 7496, 42, poll_interval=2)

Develop
=======

Contributions are welcome! For developement you can build the extension in the
current dir::

    $ python setup.py build_ext --build-lib .

To regenerate the SWIG wrappers (SWIG 2.0+ required), in the IB API directory
run::

    $ swig -v -c++ -python -threads -keyword -w511 -o swig_wrap.cpp 
        -outdir .. -modern -fastdispatch -nosafecstrings -noproxydel 
        -fastproxy -fastinit -fastunpack -fastquery -modernargs -nobuildnone 
        ../swigify_ib.i

**NOTE:** SWIG options -builtin and -fvirtual are not compatible with swigibpy's
interface file.

License
=======

swigibpy original code is free software under the New BSD license.

Interactive Brokers propriety C++ API is copyright Interactive Brokers LLC.
swigibpy is in no way supported or endorsed by Interactive Brokers LLC.

--------------

.. _Interactive Brokers: http://www.interactivebrokers.co.uk/
.. _SWIG: http://www.swig.org/
.. _C++ API documentation: http://www.interactivebrokers.com/en/p.php?f=programInterface
.. _MinGW: http://www.mingw.org/
.. _add MinGW to your path: http://www.mingw.org/wiki/Getting_Started#toc5
.. _compatability problem: http://bugs.python.org/issue12641
.. _here: https://github.com/Komnomnomnom/swigibpy/issues/2
