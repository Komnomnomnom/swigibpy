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

/* Customise EPosixClientSocket so that TWS is automatically polled for messages when we are connected to it */
%pythoncode %{
import sys
import threading
import select
from traceback import print_exc, print_exception


class TWSPoller(threading.Thread):
    '''Continually polls TWS for any outstanding messages.

    Loops indefinitely until killed or a fatal error is encountered. Uses
    socket select to poll for input and calls TWS's
    `EClientSocketBase::checkMessages` function.
    '''

    def __init__(self, tws, wrapper):
        super(TWSPoller, self).__init__()
        self.daemon = True
        self._tws = tws
        self._wrapper = wrapper

    def run(self):
        '''Continually poll TWS'''
        fd = self._tws.fd()
        pollin = [fd]
        pollout = []
        pollerr = [fd]

        while self._tws and self._tws.isConnected():
            try:
                evts = select.select(pollin, pollout, pollerr)
            except select.error:
                break
            else:
                if fd in evts[0]:
                    try:
                        while self._tws.checkMessages():
                            pass
                    except (SystemExit, SystemError, KeyboardInterrupt):
                        break
                    except:
                        try:
                            self._wrapper.pyError(*sys.exc_info())
                        except:
                            print_exc()
                else:
                    break
%}

%feature("pythonappend") EPosixClientSocket::EPosixClientSocket(EWrapper *ptr) %{
        # store a reference to EWrapper on the Python side (C++ member is protected so inaccessible from Python).
        self._ewrapper = ptr
%}
%feature("shadow") EClientSocketBase::eConnect(const char *host, unsigned int port, int clientId=0, bool extraAuth=false) %{
    def eConnect(self, host, port, clientId=0, extraAuth=False, poll_auto=True):
        val = _swigibpy.EPosixClientSocket_eConnect(self, host, port, clientId, extraAuth)
        if poll_auto and val:
            self.poller = TWSPoller(self, self._ewrapper)
            self.poller.start()
        return val
%}
%include "src/EPosixClientSocket.h"

%feature("shadow") EWrapper::winError(const IBString &, int) %{
    def winError(self, str, lastError):
        '''Error in TWS API library'''
        sys.stderr.write("TWS Error - %s: %s\n" % (lastError, str))
%}
%feature("shadow") EWrapper::error(const int, const int, const IBString) %{
    def error(self, id, errorCode, errorString):
        '''Error during communication with TWS'''
        if errorCode == 165: # Historical data sevice message
            sys.stderr.write("TWS Warning - %s: %s\n" % (errorCode, errorString))
        elif errorCode >= 501 and errorCode < 600: # Socket read failed
            sys.stderr.write("TWS Client Error - %s: %s\n" % (errorCode, errorString))
        elif errorCode >= 100 and errorCode < 1100:
            sys.stderr.write("TWS Error - %s: %s\n" % (errorCode, errorString))
        elif errorCode >= 1100 and errorCode < 2100:
            sys.stderr.write("TWS System Error - %s: %s\n" % (errorCode, errorString))
        elif errorCode >= 2100 and errorCode <= 2110:
            sys.stderr.write("TWS Warning - %s: %s\n" % (errorCode, errorString))
        else:
            sys.stderr.write("TWS Error - %s: %s\n" % (errorCode, errorString))
%}

%extend EWrapper {
%pythoncode {
    def pyError(self, type, value, traceback):
        sys.stderr.write("Exception thrown during EWrapper method dispatch:\n")
        print_exception(type, value, traceback)
}
}
%include "shared/EWrapper.h"

%pythoncode  %{

class EWrapperVerbose(EWrapper):
    def _print_call(self, name, *args, **kwargs):
        argspec = []
        if args:
            argspec.append(', '.join(str(a) for a in args))
        if kwargs:
            argspec.append(', '.join('%s=%s' for k, v in kwargs.items()))
        print('TWS call ignored - %s(%s)' % (name, ', '.join(argspec)))

class EWrapperQuiet(EWrapper):
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
