'''Simple example of using the SWIG generated TWS wrapper to request historical 
data from interactive brokers.

Note:
* The TWS C++ API needs to be polled for messages every second or so, this can
be done using a dedicated thread, as shown below.
* Communication with TWS is asynchronous; requests to TWS are made through the 
EPosixClientSocket class and TWS responds at some later time via the functions 
in our EWrapper subclass.
* If you're using a demo account TWS will only respond with a limited time
period, no matter what is requested. Also the data returned is probably wholly
unreliable.

'''

from datetime import datetime
import threading
import time

from swigibpy import EWrapper, EPosixClientSocket, Contract


class Poller(threading.Thread):
    '''Polls TWS every second for any outstanding messages'''
    
    def __init__(self, tws):
        threading.Thread.__init__(self)
        self._tws = tws
        self.stop_polling = False
    
    def run(self):
        '''Continually poll TWS until the stop flag is set'''
         
        while not self.stop_polling:
            self._tws.checkMessages()
            time.sleep(1)
            
        # Clean up connection
        tws.eDisconnect()
         

class HistoricalDataExample(EWrapper):
    '''Callback object passed to TWS, these functions will be called directly 
    by TWS.
    
    '''
    
    def __init__(self): 
        EWrapper.__init__(self)
        self.poller = None

    def nextValidId(self, orderId):
        '''Always called by TWS but not relevant for our example'''
        pass
    
    def openOrderEnd(self):
        '''Always called by TWS but not relevant for our example'''
        pass

    def historicalData(self, reqId, date, open, high, \
                       low, close, volume, \
                       barCount, WAP, hasGaps):
        
        if date[:8] == 'finished':
            print "History request complete"
            
            # Request finished, stop the poll thread
            if self.poller is not None:
                self.poller.stop_polling = True
        else:
            date = datetime.strptime(date, "%Y%m%d").strftime("%d %b %Y")
            print ( "History %s - Open: %s, High: %s, Low: %s, Close: " +
                    "%s, Volume: %d" ) % (date, open, high, low, close, volume)


# Instantiate our callback object
callback = HistoricalDataExample()

# Instantiate a socket object, allowing us to call TWS directly. Pass our
# callback object so TWS can respond.
tws = EPosixClientSocket(callback)

# Start the polling thread
poll = Poller(tws)
callback.poller = poll
poll.start()

try:

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
    
    
except:
    # Stop the poll thread if an exception occurs
    poll.stop_polling = True
    raise
    
    

