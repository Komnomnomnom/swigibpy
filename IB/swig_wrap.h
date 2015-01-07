/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 3.0.2
 *
 * This file is not intended to be easily readable and contains a number of
 * coding conventions designed to improve portability and efficiency. Do not make
 * changes to this file unless you know what you are doing--modify the SWIG
 * interface file instead.
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_swigibpy_WRAP_H_
#define SWIG_swigibpy_WRAP_H_

#include <map>
#include <string>


class SwigDirector_EWrapper : public EWrapper, public Swig::Director {

public:
    SwigDirector_EWrapper(PyObject *self);
    virtual ~SwigDirector_EWrapper();
    virtual void tickPrice(TickerId tickerId, TickType field, double price, int canAutoExecute);
    virtual void tickSize(TickerId tickerId, TickType field, int size);
    virtual void tickOptionComputation(TickerId tickerId, TickType tickType, double impliedVol, double delta, double optPrice, double pvDividend, double gamma, double vega, double theta, double undPrice);
    virtual void tickGeneric(TickerId tickerId, TickType tickType, double value);
    virtual void tickString(TickerId tickerId, TickType tickType, IBString const &value);
    virtual void tickEFP(TickerId tickerId, TickType tickType, double basisPoints, IBString const &formattedBasisPoints, double totalDividends, int holdDays, IBString const &futureExpiry, double dividendImpact, double dividendsToExpiry);
    virtual void orderStatus(OrderId orderId, IBString const &status, int filled, int remaining, double avgFillPrice, int permId, int parentId, double lastFillPrice, int clientId, IBString const &whyHeld);
    virtual void openOrder(OrderId orderId, Contract const &arg0, Order const &arg1, OrderState const &arg2);
    virtual void openOrderEnd();
    virtual void winError(IBString const &str, int lastError);
    virtual void connectionClosed();
    virtual void updateAccountValue(IBString const &key, IBString const &val, IBString const &currency, IBString const &accountName);
    virtual void updatePortfolio(Contract const &contract, int position, double marketPrice, double marketValue, double averageCost, double unrealizedPNL, double realizedPNL, IBString const &accountName);
    virtual void updateAccountTime(IBString const &timeStamp);
    virtual void accountDownloadEnd(IBString const &accountName);
    virtual void nextValidId(OrderId orderId);
    virtual void contractDetails(int reqId, ContractDetails const &contractDetails);
    virtual void bondContractDetails(int reqId, ContractDetails const &contractDetails);
    virtual void contractDetailsEnd(int reqId);
    virtual void execDetails(int reqId, Contract const &contract, Execution const &execution);
    virtual void execDetailsEnd(int reqId);
    virtual void error(int const id, int const errorCode, IBString const errorString);
    virtual void updateMktDepth(TickerId id, int position, int operation, int side, double price, int size);
    virtual void updateMktDepthL2(TickerId id, int position, IBString marketMaker, int operation, int side, double price, int size);
    virtual void updateNewsBulletin(int msgId, int msgType, IBString const &newsMessage, IBString const &originExch);
    virtual void managedAccounts(IBString const &accountsList);
    virtual void receiveFA(faDataType pFaDataType, IBString const &cxml);
    virtual void historicalData(TickerId reqId, IBString const &date, double open, double high, double low, double close, int volume, int barCount, double WAP, int hasGaps);
    virtual void scannerParameters(IBString const &xml);
    virtual void scannerData(int reqId, int rank, ContractDetails const &contractDetails, IBString const &distance, IBString const &benchmark, IBString const &projection, IBString const &legsStr);
    virtual void scannerDataEnd(int reqId);
    virtual void realtimeBar(TickerId reqId, long time, double open, double high, double low, double close, long volume, double wap, int count);
    virtual void currentTime(long time);
    virtual void fundamentalData(TickerId reqId, IBString const &data);
    virtual void deltaNeutralValidation(int reqId, UnderComp const &underComp);
    virtual void tickSnapshotEnd(int reqId);
    virtual void marketDataType(TickerId reqId, int marketDataType);
    virtual void commissionReport(CommissionReport const &commissionReport);
    virtual void position(IBString const &account, Contract const &contract, int position);
    virtual void positionEnd();
    virtual void accountSummary(int reqId, IBString const &account, IBString const &tag, IBString const &value, IBString const &curency);
    virtual void accountSummaryEnd(int reqId);

/* Internal director utilities */
public:
    bool swig_get_inner(const char *swig_protected_method_name) const {
      std::map<std::string, bool>::const_iterator iv = swig_inner.find(swig_protected_method_name);
      return (iv != swig_inner.end() ? iv->second : false);
    }
    void swig_set_inner(const char *swig_protected_method_name, bool val) const {
      swig_inner[swig_protected_method_name] = val;
    }
private:
    mutable std::map<std::string, bool> swig_inner;

#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::SwigVar_PyObject name = SWIG_Python_str_FromChar(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (!method) {
          std::string msg = "Method in class EWrapper doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      }
      return method;
    }
private:
    mutable swig::SwigVar_PyObject vtable[42];
#endif

};


#endif
