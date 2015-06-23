/*
    SWIG interface file for Interactive Brokers API.
*/

%module(directors="1", docstring="Python wrapper for Interactive Brokers TWS C++ API") swigibpy

/* Turn on auto-generated docstrings */
%feature("autodoc", "1");

/* auto convert std::string and typedefs to Python strings */
%include "std_string.i"
typedef std::string IBString;

/* auto convert std::vector to Python lists */
%include "std_vector.i"

/* use boost template to generate shared pointer handling */
%include <boost_shared_ptr.i>

/* Inclusions for generated cpp file */
%{
#include "shared/shared_ptr.h"

#include "shared/IBString.h"
#include "shared/EClient.h"
#include "shared/EClientSocketBase.h"

#include "src/EPosixClientSocket.h"
#include "shared/EWrapper.h"

#include "shared/CommissionReport.h"
#include "shared/CommonDefs.h"
#include "shared/Contract.h"
#include "shared/Execution.h"
#include "shared/Order.h"
#include "shared/OrderState.h"
#include "shared/ScannerSubscription.h"
#include "shared/TagValue.h"
%}


/* Shared Pointers */
%shared_ptr(ComboLeg)
%shared_ptr(std::vector<boost::shared_ptr<ComboLeg> >)

%shared_ptr(OrderComboLeg)
%shared_ptr(std::vector<boost::shared_ptr<OrderComboLeg> >)

%shared_ptr(TagValue)
%shared_ptr(std::vector<boost::shared_ptr<TagValue> >)

/* Vector (list) containers */
%template(ComboLegList) std::vector<boost::shared_ptr<ComboLeg> >;
%template(OrderComboLegList) std::vector<boost::shared_ptr<OrderComboLeg> >;
%template(TagValueList) std::vector<boost::shared_ptr<TagValue> >;

/*
   TWS use their own shared_ptr class, need to fool SWIG into thinking
   it's the standard boost::shared_ptr.
   This means the generated cpp file must be post-processed to remove
   references to boost (see setup.py).
*/
#define shared_ptr boost::shared_ptr

/*EWrapper will be subclassed in Python*/
%feature("director") EWrapper;
%feature("director:except") {
    if ($error != NULL) {

        if ( !( PyErr_ExceptionMatches(PyExc_SystemExit) ||
                PyErr_ExceptionMatches(PyExc_SystemError) ||
                PyErr_ExceptionMatches(PyExc_KeyboardInterrupt) ) )
        {
            PyObject *value = 0;
            PyObject *traceback = 0;

            PyErr_Fetch(&$error, &value, &traceback);
            PyErr_NormalizeException(&$error, &value, &traceback);

            {
                swig::SwigVar_PyObject swig_method_name = SWIG_Python_str_FromChar((char *) "pyError");
                swig::SwigVar_PyObject result = PyObject_CallMethodObjArgs(swig_get_self(), (PyObject *) swig_method_name, $error, value, traceback, NULL);
            }

            Py_XDECREF($error);
            Py_XDECREF(value);
            Py_XDECREF(traceback);

            $error = PyErr_Occurred();
            if ($error != NULL) {
                PyErr_Print();
                throw Swig::DirectorMethodException();
            }
        }
        else
        {
            throw Swig::DirectorMethodException();
        }
    }
}

/* Exception handling */
%include exception.i
%exception {
    // most errors should be propagated through to EWrapper->error,
    // others should be added here as and when needed / encountered.
    try {
        $action
    } catch(Swig::DirectorPureVirtualException &e) {
        /* Call to pure virtual method, raise not implemented error */
        PyErr_SetString(PyExc_NotImplementedError, "$decl not implemented");
        SWIG_fail;
    } catch(Swig::DirectorException &e) {
        /* Fail if there is a problem in the director proxy transport */
        SWIG_fail;
    } catch(std::exception& e) {
        /* Convert standard error to Exception */
        PyErr_SetString(PyExc_Exception, const_cast<char*>(e.what()));
        SWIG_fail;
    } catch(...) {
        /* Final catch all, results in runtime error */
        PyErr_SetString(PyExc_RuntimeError, "Unknown error caught in Interactive Brokers SWIG wrapper...");
        SWIG_fail;
    }
}

/* Grab the header files to be wrapped */
%include "shared/CommissionReport.h"
%include "shared/CommonDefs.h"
%include "shared/Contract.h"
%include "shared/EClient.h"
%include "shared/EClientSocketBase.h"
%include "shared/Execution.h"
%include "shared/Order.h"
%include "shared/OrderState.h"
%include "shared/ScannerSubscription.h"
%include "shared/TagValue.h"

%pythonbegin %{
import warnings
import sys
import threading
import select
from traceback import print_exc, print_exception
%}

/* Customise EPosixClientSocket so that TWS is automatically polled for messages when we are connected to it */
%pythoncode %{

class TWSPoller(threading.Thread):
    '''Continually polls TWS for any outstanding messages.

    Loops indefinitely until killed or a system error occurs.

    Uses socket select to poll for input and calls TWS's
    `EClientSocketBase::checkMessages` function.
    '''

    MAX_BACKOFF = 5000

    def __init__(self, tws, wrapper):
        super(TWSPoller, self).__init__()
        self.daemon = True
        self._tws = tws
        self._wrapper = wrapper
        self._stop_evt = threading.Event()
        self._connected_evt = threading.Event()

        self.tws_connected(tws.isConnected())

    def stop_poller(self):
        self._stop_evt.set()

    def tws_connected(self, flag):
        if flag:
            self._connected_evt.set()
        else:
            self._connected_evt.clear()

    def run(self):
        modules = sys.modules
        try:
            self._run()
        except:
            # ignore errors raised during interpreter shutdown.
            if modules:
                raise

    def _run(self):
        '''Continually poll TWS'''
        stop = self._stop_evt
        connected = self._connected_evt
        tws = self._tws

        fd = tws.fd()
        pollfd = [fd]

        while not stop.is_set():
            while (not connected.is_set() or not tws.isConnected()) and not stop.is_set():
                connected.clear()
                backoff = 0
                retries = 0

                while not connected.is_set() and not stop.is_set():
                    if tws.reconnect_auto and not tws.reconnect():
                        if backoff < self.MAX_BACKOFF:
                            retries += 1
                            backoff = min(2**(retries + 1), self.MAX_BACKOFF)
                        connected.wait(backoff / 1000.)
                    else:
                        connected.wait(1)
                fd = tws.fd()
                pollfd = [fd]

            if fd > 0:
                try:
                    evtin, _evtout, evterr = select.select(pollfd, [], pollfd, 1)
                except select.error:
                    connected.clear()
                    continue
                else:
                    if fd in evtin:
                        try:
                            if not tws.checkMessages():
                                tws.eDisconnect(stop_polling=False)
                                continue
                        except (SystemExit, SystemError, KeyboardInterrupt):
                            break
                        except:
                            try:
                                self._wrapper.pyError(*sys.exc_info())
                            except:
                                print_exc()
                    elif fd in evterr:
                        connected.clear()
                        continue
%}

%feature("shadow") EPosixClientSocket::EPosixClientSocket(EWrapper *ptr) %{
    def __init__(self, ewrapper, poll_auto=True, reconnect_auto=False):
        '''Create an EPosixClientSocket to comunicate with Interactive Brokers.

        Parameters
        ----------
        ewrapper : EWrapper subclass to which responses will be dispatched.
        poll_auto : boolean, if True automatically poll for messages with a
            background thread. Default True
        reconnect_auto : boolean, if True automatically reconnect to TWS if
            the connection is lost. Default False
        '''
        _swigibpy.EPosixClientSocket_swiginit(self, $action(ewrapper))

        # store a reference to EWrapper on the Python side (C++ member is protected so inaccessible from Python).
        self._ewrapper = ewrapper

        self._connect_lock = threading.Lock()
        self.poller = None
        self._poll_auto = poll_auto
        self.reconnect_auto = reconnect_auto
        self._connect_args = None
%}
%feature("shadow") EClientSocketBase::eConnect(const char *host, unsigned int port, int clientId=0, bool extraAuth=false) %{
    def eConnect(self, host, port, clientId=0, extraAuth=False, **kwargs):
        if "poll_auto" in kwargs:
            warnings.warn("eConnect argument 'poll_auto' is deprecated, use 'poll_auto' arg in constructor instead", warnings.DeprecationWarning)
            self.poll_auto = kwargs.pop('poll_auto')

        with self._connect_lock:
            success = $action(self, host, port, clientId, extraAuth)

        if success:
            self._connect_args = ((host, port, clientId, extraAuth), kwargs)
        if self.isConnected():
            self._startPolling()
            if self.poller is not None:
                self.poller.tws_connected(True)
        return success
%}
%feature("shadow") EClientSocketBase::eDisconnect() %{
    def eDisconnect(self, stop_polling=True):
        if stop_polling:
            self._stopPolling()
        val = $action(self)
        if self.poller is not None:
            self.poller.tws_connected(False)
        return val
%}
%extend EPosixClientSocket {
%pythoncode {

    def reconnect(self):
        if self._connect_args is None:
            return
        return self.eConnect(*self._connect_args[0], **self._connect_args[1])

    def _startPolling(self):
        if not self.poll_auto:
            return
        if  self.poller is None or not self.poller.is_alive():
            self.poller = TWSPoller(self, self._ewrapper)
            self.poller.start()

    def _stopPolling(self):
        if self.poller is not None:
            self.poller.stop_poller()

    @property
    def poll_auto(self):
        return self._poll_auto

    @poll_auto.setter
    def poll_auto(self, val):
        self._poll_auto = val
        if val:
            self._startPolling()
        else:
            self._stopPolling()
}
}

%include "src/EPosixClientSocket.h"

%feature("shadow") EWrapper::winError(const IBString &, int) %{
    def winError(self, str, lastError):
        '''Error in TWS API library'''
        sys.stderr.write("TWS ERROR - %s: %s\n" % (lastError, str))
%}
%feature("shadow") EWrapper::error(const int, const int, const IBString) %{
    def error(self, id, errorCode, errorString):
        '''Error during communication with TWS'''
        if errorCode == 165: # Historical data sevice message
            sys.stderr.write("TWS WARNING - %s: %s\n" % (errorCode, errorString))
        elif errorCode >= 501 and errorCode < 600: # Socket read failed
            sys.stderr.write("TWS CLIENT-ERROR - %s: %s\n" % (errorCode, errorString))
        elif errorCode >= 100 and errorCode < 1100:
            sys.stderr.write("TWS ERROR - %s: %s\n" % (errorCode, errorString))
        elif errorCode >= 1100 and errorCode < 2100:
            sys.stderr.write("TWS SYSTEM-ERROR - %s: %s\n" % (errorCode, errorString))
        elif errorCode in (2104, 2106):
            sys.stderr.write("TWS INFO - %s: %s\n" % (errorCode, errorString))
        elif errorCode >= 2100 and errorCode <= 2110:
            sys.stderr.write("TWS WARNING - %s: %s\n" % (errorCode, errorString))
        else:
            sys.stderr.write("TWS ERROR - %s: %s\n" % (errorCode, errorString))
%}

%extend EWrapper {
%pythoncode {
    def pyError(self, type, value, traceback):
        '''Handles an error thrown during invocation of an EWrapper method.

        Arguments are those provided by sys.exc_info()
        '''
        sys.stderr.write("Exception thrown during EWrapper method dispatch:\n")
        print_exception(type, value, traceback)
}
}
%include "shared/EWrapper.h"

%pythoncode  %{

class EWrapperVerbose(EWrapper):
    '''Implements all EWrapper methods and prints to standard out when a method
    is invoked.
    '''

    def _print_call(self, name, *args, **kwargs):
        argspec = []
        if args:
            argspec.append(', '.join(str(a) for a in args))
        if kwargs:
            argspec.append(', '.join('%s=%s' for k, v in kwargs.items()))
        print('TWS call ignored - %s(%s)' % (name, ', '.join(argspec)))

class EWrapperQuiet(EWrapper):
    '''Implements all EWrapper methods and ignores method calls.'''

    def _ignore_call(self, *args, **kwargs):
        pass

def _make_printer(name):
    return lambda self, *a, **kw: self._print_call(name, *a, **kw)

for name, attr in EWrapper.__dict__.items():
    if name[0] == '_' or not callable(attr) or name in ('error', 'winError', 'pyError'):
        continue

    setattr(EWrapperQuiet, name, EWrapperQuiet.__dict__['_ignore_call'])
    setattr(EWrapperVerbose, name, _make_printer(name))
%}
