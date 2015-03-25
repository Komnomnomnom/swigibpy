swigibpy
========

:version: 0.5.0

An `Interactive Brokers`_ Python API, auto-generated from the official C++ API
using `SWIG`_.

Installation
============

Use pip (recommended)

.. code:: sh

    pip install swigibpy

Alternatively download `a release`_, extract it and run

.. code:: sh

    python setup.py install

Getting Started
===============

TWS or IB Gateway must be running. To use **swigibpy** simply import the
``swigibpy`` module into your code, define an ``EWrapper`` sub-class and create
a ``swigibpy.EPosixClientSocket`` instance.

Use the methods of your ``swigibpy.EPosixClientSocket`` instance to send
requests to Interactive Brokers. All requests are asynchronous and any
responses, notifications and warnings are handled by the methods of your
``EWrapper`` subclass.

In the following simple example a request is made to Interactive Brokers for
some historical data for the GOOG ticker, and the response is printed to the
console.

.. code:: python

  from datetime import datetime

  import swigibpy


  class MyEWrapper(swigibpy.EWrapperVerbose):

      def historicalData(self, reqId, date, open, high, low, close, volume,
			 barCount, WAP, hasGaps):

        if date[:8] == 'finished':
            print("History request complete")
        else:
            date = datetime.strptime(date, "%Y%m%d").strftime("%d %b %Y")
            print(("History %s - Open: %s, High: %s, Low: %s, Close: "
                   "%s, Volume: %d") % (date, open, high, low, close, volume))

  myWrapper = MyEWrapper()

  tws = swigibpy.EPosixClientSocket(myWrapper, reconnect_auto=True)

  tws.eConnect("", 7496, 42)

  contract = swigibpy.Contract()
  contract.exchange = "SMART"
  contract.symbol = "GOOG"
  contract.secType = "STK"
  contract.currency = "USD"
  today = datetime.today()

  tws.reqHistoricalData(2, contract, today.strftime("%Y%m%d %H:%M:%S %Z"),
                        "1 W", "1 day", "TRADES", 0, 1, None)



See the `examples`_ for some more simple demos of using **swigibpy**. For a
more in-depth introduction Rob Carver has written a nice series of blog posts
on `getting started with swigibpy and the Interative Brokers API`_.

For documentation on the methods of ``EPosixClientSocket``, ``EWrapper`` and
other API reference refer to the `C++ API documentation`_.

Note that unlike the C++ API **swigibpy** will automatically poll
TWS for messages, see `Message Polling`_ for more about this.

Error Handling
--------------

If TWS reports an error then the ``EWrapper`` methods ``error`` and
``winError`` will be called as described in the TWS `C++ API documentation`_.

Additionally **swigibpy** augments ``EWrapper`` with an extra error handling
method.

.. code:: python

  def pyError(self, type, value, traceback)

which will be called if an exception is raised during execution of one of your
``EWrapper`` Python methods. The default behaviour is to print the exception to
standard error, but you can override the ``pyError`` method to implement your own
handling.  See the `python docs for sys.exc_info()`_ for details on the
method's arguments.

EWrapper Utility Classes
------------------------

Normally subclassing ``EWrapper`` means having to tiresomely provide an
implementation for every method defined by ``EWrapper``. Happily **swigibpy**
adds two ``EWrapper`` subclasses which can help.

``EWrapperVerbose`` implements every ``EWrapper`` method and by default just
prints a message to standard out every time one of its methods is invoked. The
message printed includes the arguments that were passed. Useful for development
and debugging.

``EWrapperQuiet`` implements every ``EWrapper`` method and silently ignores
any calls that have not been implemented by you. Useful if you are not
interested in defining every ``EWrapper`` method.

Auto-reconnect
--------------

**swigibpy** can automatically reconnect to TWS / IB Gateway in case of
connection loss or restart. To enable this behaviour use the ``reconnect_auto``
argument added to ``EPosixClientSocket``.

.. code:: python

    tws = EPosixClientSocket(mywrapper, reconnect_auto=True)

Auto-reconnect is disabled by default.

Notes
-----

The ``yield`` parameter in ``CommissionReport`` clashes with a Python reserved
keyword so it is renamed to ``_yield``.

Advanced Usage
--------------

Message Polling
+++++++++++++++

By default **swigibpy** will create a background thread (``swigibpy.TWSPoller``)
to automatically poll TWS for messages.  If you wish to disable this behaviour
and handle polling yourself use the ``poll_auto`` argument added to
``EPosixClientSocket``

.. code:: python

    tws = EPosixClientSocket(mywrapper, poll_auto=False)

or

.. code:: python

    tws = EPosixClientSocket(mywrapper)
    ...
    tws.poll_auto = False

The TWS C++ API performs non-blocking socket I/O to communicate with TWS,
**swigibpy**'s background thread uses socket select to poll for incoming messages.


Patches
+++++++

Apart from a few trivial `patches`_ to aid compilation and interoperability
with Python **swigibpy** does not alter the TWS C++ API code in any way.

Contribute
==========

**swigibpy** is open source so feel free to get involved. If something doesn't
work, or you'd like to add a feature, example or some documentation please
`create a pull request`_, if you need help `open an issue`_.

For development switch to the swigibpy code directory and build the extension
in the current dir.

.. code:: sh

     python setup.py build_ext --inplace

Apart from the `patches`_ all of **swigibpy**'s code is defined in a SWIG
`interface file`_. The C++ and Python wrapper is then generated using SWIG.

The TWS API included in the repository has already been patched and the
repository already includes the SWIG generated code but if you modify the
interface file or need to rerun these steps the commands are

.. code:: sh

    python setup.py swigify

to regenerate the SWIG wrappers (SWIG 3.0+ required), and

.. code:: sh

    python setup.py patchify

to reapply the patches to the TWS API (specify the option ``-r`` if you want to 
un-apply the patches and get back to unaltered TWS code).

Windows Users
=============

**swigibpy** provides a wrapper around the TWS C++ API so it must be
compiled for your target platform during installation. While this should
'just work' for Linux and OSX, Windows users might need to do some extra work.

Only some basic tips are given here, for more see `Installing Python Modules`_
in the official documentation.

MinGW Compilation
-----------------

Download and install `MinGW`_ and follow the steps to `add MinGW
to your path`_.

To get pip to use MinGW as the compiler edit or create a
file named ``distutils.cfg`` in ``[PYTHON LOCATION]\Lib\distutils`` where
``[PYTHON LOCATION]`` is the path to your Python install, e.g. ``C:\Python27``.
Add the following to ``distutils.cfg``.

.. code:: cfg

	[build]
	compiler=mingw32

then use the pip command given above in `Installation`_ and with a bit of luck,
you're done!

Alternatively you can download `a release`_ and build the package directly. To
build and install manually use

.. code:: sh

	python setup.py build -c mingw32
	python setup.py install

This has been verified to work using MinGW and Python 2.7 on Windows 7, Vista,
and XP.

Visual Studio Compilation
-------------------------

Several users have reported success building **swigibpy** with Visual Studio,
with a few caveats:

* Distutils has issues building with anything later than Visual Studio 2008
  (version 9).
* Visual Studio 11 doesn't like the ``/MD`` compile flag, which distutils adds.
  For a workaround see `here`_.

License
=======

**swigibpy** original code is free software under the `New BSD license`_.

Interactive Brokers propriety C++ API is copyright Interactive Brokers LLC.
**swigibpy** is in no way supported or endorsed by Interactive Brokers LLC.

--------------

.. _Interactive Brokers: http://www.interactivebrokers.com/
.. _SWIG: http://www.swig.org/
.. _a release: https://github.com/Komnomnomnom/swigibpy/releases
.. _C++ API documentation: http://www.interactivebrokers.com/en/software/api/api.htm
.. _MinGW: http://www.mingw.org/
.. _add MinGW to your path: http://www.mingw.org/wiki/Getting_Started#toc7
.. _here: https://github.com/Komnomnomnom/swigibpy/issues/2
.. _patches: https://github.com/Komnomnomnom/swigibpy/tree/master/patches
.. _examples: https://github.com/Komnomnomnom/swigibpy/tree/master/examples
.. _getting started with swigibpy and the Interative Brokers API: http://qoppac.blogspot.co.uk/2014/03/using-swigibpy-so-that-python-will-play.html
.. _python docs for sys.exc_info(): https://docs.python.org/2/library/sys.html#sys.exc_info
.. _open an issue: https://github.com/Komnomnomnom/swigibpy/issues
.. _create a pull request: https://github.com/Komnomnomnom/swigibpy/pulls
.. _Installing Python Modules: https://docs.python.org/2/install/
.. _New BSD License: https://github.com/Komnomnomnom/swigibpy/blob/master/LICENSE
.. _interface file: https://github.com/Komnomnomnom/swigibpy/blob/master/swigify_ib.i
