Overview
========

`Interactive Brokers`_ Python API, auto generated from C++ API using `SWIG`_.

Latest version: 0.2.2 (TWS API v9.65)

Windows Prerequisites
=====================

swigibpy just provides a wrapper around the TWS C++ API so this needs to be 
compiled for your target platform during installation. While this should 
'just work' for Linux and OSX, Windows users might need to do some extra work.

If you have Visual Studio, it might 'just work'. Please let me know if it 
does or doesn't!

Otherwise download and install `MinGW`_ and follow the steps to `add MinGW 
to your path`_. To get pip to use MinGW as the compiler edit or create a 
file named ``distutils.cfg`` in ``[PYTHON LOCATION]\Lib\distutils`` where
``[PYTHON LOCATION]`` is the path to your Python install, e.g. ``C:\Python27``.
Add the following to ``distutils.cfg``::

	[build]
	compiler=mingw32

This has been tested using MinGW and Python 2.7 on Windows Vista.	

Install
=======

Use pip (recommended)::

    $ pip install swigibpy
    
Alternatively download your archive of choice and run::

    $ python setup.py install
    
Usage
=====

To use simply import the swigibpy module, see the examples directory for more.
For API reference refer to the `C++ API documentation`_. 

Develop
=======
    
Contributions are welcome! For developement you can build the extension in the
current dir::

    $ python setup.py build_ext --build-lib .
 
To regenerate the SWIG wrappers (SWIG 2.0+ required), in the IB API directory
run::

    $ swig -v -c++ -python -threads -o swig_wrap.cpp -outdir .. -modern 
        -fastdispatch -nosafecstrings -noproxydel -fastproxy -fastinit
        -fastunpack -fastquery -modernargs -nobuildnone ../swigify_ib.i
        
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
