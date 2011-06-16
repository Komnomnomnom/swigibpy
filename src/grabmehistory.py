'''
Created on Jun 15, 2011

@author: kieran
'''

import ib
import time
import threading

class SOBWrapper(ib.EWrapper):
    def __init__(self): 
        ib.EWrapper.__init__(self)

    def winError(self, str, lastError):
        print "WinError", lastError, str

    def error(self, id, errorCode, errorString):
        print "Error", id, errorCode, errorString

    def nextValidId(self, orderId):
        print "nextValidId, orderId =", orderId

    def openOrderEnd(self):
        print "openOrderEnd"

    def historicalData(self, reqId, date, open, high, \
                       low, close, volume, \
                       barCount, WAP, hasGaps):
        print "History ->", date

    def tickPrice(self, *args):
        print "tickPrice"

    def tickSize(self, *args):
        print "tickSize"

    def tickOptionComputation(self, *args):
        print "tickOptionComputation"

    def tickGeneric(self, *args):
        print "tickGeneric"

    def tickString(self, *args):
        print "tickString"

    def tickEFP(self, *args):
        print "tickEFP"

    def orderStatus(self, *args):
        print "orderStatus"

    def openOrder(self, *args):
        print "openOrder"

    def connectionClosed(self):
        print "connectionClosed"

    def updateAccountValue(self, *args):
        print "updateAccountValue"

    def updatePortfolio(self, *args):
        print "updatePortfolio"

    def updateAccountTime(self, *args):
        print "updateAccountTime"

    def accountDownloadEnd(self, *args):
        print "accountDownloadEnd"

    def contractDetails(self, *args):
        print "contractDetails"

    def bondContractDetails(self, *args):
        print "bondContractDetails"

    def contractDetailsEnd(self, *args):
        print "contractDetailsEnd"

    def execDetails(self, *args):
        print "execDetails"

    def execDetailsEnd(self, *args):
        print "execDetailsEnd"

    def updateMktDepth(self, *args):
        print "updateMktDepth"

    def updateMktDepthL2(self, *args):
        print "updateMktDepthL"

    def updateNewsBulletin(self, *args):
        print "updateNewsBulletin"

    def managedAccounts(self, *args):
        print "managedAccounts"

    def receiveFA(self, *args):
        print "receiveFA"

    def scannerParameters(self, *args):
        print "scannerParameters"

    def scannerData(self, *args):
        print "scannerData"

    def scannerDataEnd(self, *args):
        print "scannerDataEnd"

    def realtimeBar(self, *args):
        print "realtimeBar"

    def currentTime(self, *args):
        print "currentTime"

    def fundamentalData(self, *args):
        print "fundamentalData"

    def deltaNeutralValidation(self, *args):
        print "deltaNeutralValidation"

    def tickSnapshotEnd(self, *args):
        print "tickSnapshotEnd"


            
wrap = SOBWrapper()
tws = ib.EPosixClientSocket(wrap)

#connect to tws running on localhost
tws.eConnect("", 7496, 42)

#turn on detailed logging
tws.setServerLogLevel(5)

tws.checkMessages()

# Simple contract for DELL
dell = ib.Contract()
dell.exchange = "SMART"
dell.symbol = "DELL"
dell.secType = "STK"
dell.currency = "USD"

print "Requesting history"

# Request some historical data. 
tws.reqHistoricalData(
        1,                             #tickerId, 
        dell,                         #contract, 
        "20110616 09:49:00 GMT",    #endDateTime, 
        "1 W",                        #durationStr, 
        "1 day",                    #barSizeSetting, 
        "TRADES",                    #whatToShow, 
        0,                            #useRTH, 
        1                            #formatDate
    )

# unlike the Java API the C++ API needs to be polled for messages
tws.checkMessages()

#clean up connections
tws.eDisconnect()
