'''Simple example of using the SWIG generated TWS wrapper to request historical 
data from interactive brokers.

Note:
* Communication with TWS is asynchronous; requests to TWS are made through the 
EPosixClientSocket class and TWS responds at some later time via the functions 
in our EWrapper subclass.
* If you're using a demo account TWS will only respond with a limited time
period, no matter what is requested. Also the data returned is probably wholly
unreliable.

'''

from datetime import datetime
import time

from swigibpy import EWrapper, EPosixClientSocket, Contract

###

class HistoricalDataExample(EWrapper):
    '''Callback object passed to TWS, these functions will be called directly 
    by TWS.
    
    '''
    
    def nextValidId(self, orderId):
        '''Always called by TWS but not relevant for our example'''
        pass
    
    def openOrderEnd(self):
        '''Always called by TWS but not relevant for our example'''
        pass

    def historicalData(self, reqId, date, open, high, 
                       low, close, volume,
                       barCount, WAP, hasGaps):
        
        if date[:8] == 'finished':
            print "History request complete"
        else:
            date = datetime.strptime(date, "%Y%m%d").strftime("%d %b %Y")
            print ( "History %s - Open: %s, High: %s, Low: %s, Close: " +
                    "%s, Volume: %d" ) % (date, open, high, low, close, volume)


# Instantiate our callback object
callback = HistoricalDataExample()

# Instantiate a socket object, allowing us to call TWS directly. Pass our
# callback object so TWS can respond.
tws = EPosixClientSocket(callback)

# Connect to tws running on localhost
tws.eConnect("", 7496, 42)

# Simple contract for DELL
dell = Contract()
dell.exchange = "SMART"
dell.symbol = "DELL"
dell.secType = "STK"
dell.currency = "USD"
today = datetime.today()

print "Requesting historical data for %s" % dell.symbol

# Request some historical data. 
tws.reqHistoricalData(
        1,                                          #tickerId, 
        dell,                                       #contract, 
        today.strftime("%Y%m%d %H:%M:%S %Z"),       #endDateTime, 
        "1 W",                                      #durationStr, 
        "1 day",                                    #barSizeSetting, 
        "TRADES",                                   #whatToShow, 
        0,                                          #useRTH, 
        1                                           #formatDate
    )


print "\n====================================================================="
print " History requested, waiting for TWS responses"
print "=====================================================================\n"
    
    
print "******************* Press ENTER to quit when done *******************\n"
raw_input()

print "\nDisconnecting..."
tws.eDisconnect()
time.sleep(1)