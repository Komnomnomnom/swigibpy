/*
	SWIG interface file for Interactive Brokers API v9.65.
	
*/

%module(directors="1",docstring="Python wrapper for Interactive Brokers TWS C++ API") swigibpy

/* Turn on auto-generated docstrings */
%feature("autodoc", "1");

/*Inclusions for generated cpp file*/
%{
#include "Shared/EClient.h"
#include "Shared/EClientSocketBase.h"

#include "PosixSocketClient/EPosixClientSocket.h"
#include "Shared/EWrapper.h"

#include "Shared/CommonDefs.h"
#include "Shared/Contract.h"
#include "Shared/Execution.h"
#include "Shared/Order.h"
#include "Shared/OrderState.h"
#include "Shared/ScannerSubscription.h"
%}

/* auto convert std::string and typedefs to Python strings */
%include "std_string.i"
typedef std::string IBString;

/*EWrapper will be subclassed in Python*/
%feature("director") EWrapper;
%feature("director:except") {
    if ($error != NULL) {
        throw Swig::DirectorMethodException();
    }
}

// Exception handling 
%include exception.i     
%exception {
	/*
		most errors should be propagated through to EWrapper->error,
    	others should be added here as and when needed / encountered.
    */
    try {
        $action
    } catch(Swig::DirectorPureVirtualException &e) {
    	/* Call to pure virtual method, raise not implemented error */
    	PyErr_SetString(PyExc_NotImplementedError, e.getMessage());
    } catch(Swig::DirectorException &e) {
		/* Fail if there is a problem in the director proxy transport */
	    SWIG_fail;
    } catch(std::exception& e) {
    	/* Convert standard error to standard error */
        PyErr_SetString(PyExc_StandardError, const_cast<char*>(e.what()));
    
    } catch(...) {
    	/* Final catch all, results in runtime error */ 
        PyErr_SetString(PyExc_RuntimeError, "Unknown error caught in Interactive Brokers SWIG wrapper...");
    }
} 

/* Grab the header files to be wrapped */
%include "Shared/CommonDefs.h"
%include "Shared/Contract.h"
%include "Shared/EClient.h"
%include "Shared/EClientSocketBase.h"
%include "Shared/Execution.h"
%include "Shared/Order.h"
%include "Shared/OrderState.h"
%include "Shared/ScannerSubscription.h"


/* Customise EPosixClientSocket so that TWS is automatically polled for messages when we are connected to it */
%pythoncode %{
import threading
import time
class TWSPoller(threading.Thread):
    '''Polls TWS every second for any outstanding messages'''
    
    def __init__(self, tws):
        super(TWSPoller, self).__init__()
        self.daemon = True
        self._tws = tws
        self.stop_polling = False
    
    def run(self):
        '''Continually poll TWS until the stop flag is set'''
        while not self.stop_polling:
            try:
                self._tws.checkMessages()
            except:
                if self.stop_polling:
                    break
                else:
                    raise
            time.sleep(1)
%}
%pythonappend EClientSocketBase::eConnect(const char *host, unsigned int port, int clientId=0) %{
    if val:
        self.poller = TWSPoller(self)
        self.poller.start()
%}
%pythonprepend EPosixClientSocket::eDisconnect() %{
    if self.poller:
        self.poller.stop_polling = True
        self.poller = None
%}
%include "PosixSocketClient/EPosixClientSocket.h"

/* Override EWrapper's error methods  with default implementations */
%pythoncode %{
class TWSError(Exception):
    '''Exception raised during communication with Interactive Brokers TWS 
    application
    '''
    
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        
    def __str__(self):
        return "%s: %s" % (self.code, repr(self.msg))

class TWSSystemError(TWSError):
    '''System related exception raised during communication with Interactive 
    Brokers TWS application.
    '''
    pass
    
class TWSClientError(TWSError):
    '''Exception raised on client (python) side by Interactive Brokers API'''
    pass
%}
%feature("shadow") EWrapper::winError(const IBString &, int) %{
    def winError(self, str, lastError):
        '''Error in TWS API library'''
        
        raise TWSClientError(lastError, str)
%}
%feature("shadow") EWrapper::error(const int, const int, const IBString) %{
    def error(self, id, errorCode, errorString):
        '''Error during communication with TWS'''
        
        if errorCode == 165:
            print "TWS Message %s: %s" % (errorCode, errorString)
        elif errorCode >= 100 and errorCode < 1100:
            raise TWSError(errorCode, errorString)
        elif  errorCode >= 1100 and errorCode < 2100:
            raise TWSSystemError(errorCode, errorString)
        elif errorCode >= 2100 and errorCode < 2110:
            import sys
            sys.stderr.write("TWS Warning %s: %s\n" % (errorCode, errorString))
        else:
            raise RuntimeError(errorCode, errorString)
%}
%include "Shared/EWrapper.h"
