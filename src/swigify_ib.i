/*
	SWIG interface file for Interactive Brokers API v9.64.
	
	author: Kieran O'Mahony
*/

%module(directors="1") ib

/*Inclusions for generated cpp file*/
%{
#include "Shared/EClient.h"
#include "Shared/EClientSocketBase.h"

#include "PosixSocketClient/EPosixClientSocket.h"
#include "Shared/EWrapper.h"

#include "Shared/Contract.h"
#include "Shared/CommonDefs.h"

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

/* exception handling 
TODO add more catches, not everything should result in a fatal runtime error
*/
%include exception.i     
%exception {
    try {
        $action
    } catch(std::exception& e) {
        SWIG_exception(SWIG_RuntimeError,e.what());
    } catch(Swig::DirectorException &e) {
        SWIG_exception(SWIG_RuntimeError,e.getMessage());
    } catch(...) {
        SWIG_exception(SWIG_RuntimeError,"Unknown exception...");
    }
} 

/* Grab the header files to be wrapped */
%include "Shared/EClient.h"
%include "Shared/EClientSocketBase.h"

%include "PosixSocketClient/EPosixClientSocket.h"
%include "Shared/EWrapper.h"

%include "Shared/Contract.h"
%include "Shared/CommonDefs.h"
