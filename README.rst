Overview
========

`Interactive Brokers`_ Python API, auto generated from C++ API using `SWIG`_.

Latest version: 0.2.1 (TWS API v9.65)

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