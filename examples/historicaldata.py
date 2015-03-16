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
from threading import Event

from swigibpy import EWrapper, EPosixClientSocket, Contract


WAIT_TIME = 10.0

###


class HistoricalDataExample(EWrapper):
    '''Callback object passed to TWS, these functions will be called directly
    by TWS.

    '''

    def __init__(self):
        super(HistoricalDataExample, self).__init__()
        self.got_history = Event()

    def orderStatus(self, id, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFilledPrice, clientId, whyHeld):
        pass

    def openOrder(self, orderID, contract, order, orderState):
        pass

    def nextValidId(self, orderId):
        '''Always called by TWS but not relevant for our example'''
        pass

    def openOrderEnd(self):
        '''Always called by TWS but not relevant for our example'''
        pass

    def managedAccounts(self, openOrderEnd):
        '''Called by TWS but not relevant for our example'''
        pass

    def historicalData(self, reqId, date, open, high,
                       low, close, volume,
                       barCount, WAP, hasGaps):

        if date[:8] == 'finished':
            print("History request complete")
            self.got_history.set()
        else:
            date = datetime.strptime(date, "%Y%m%d").strftime("%d %b %Y")
            print(("History %s - Open: %s, High: %s, Low: %s, Close: "
                   "%s, Volume: %d") % (date, open, high, low, close, volume))


# Instantiate our callback object
callback = HistoricalDataExample()

# Instantiate a socket object, allowing us to call TWS directly. Pass our
# callback object so TWS can respond.
tws = EPosixClientSocket(callback)

# Connect to tws running on localhost
if not tws.eConnect("", 7496, 42):
    raise RuntimeError('Failed to connect to TWS')

# Simple contract for GOOG
contract = Contract()
contract.exchange = "SMART"
contract.symbol = "GOOG"
contract.secType = "STK"
contract.currency = "USD"
today = datetime.today()

print("Requesting historical data for %s" % contract.symbol)

# Request some historical data.
tws.reqHistoricalData(
    2,                                          # tickerId,
    contract,                                   # contract,
    today.strftime("%Y%m%d %H:%M:%S %Z"),       # endDateTime,
    "1 W",                                      # durationStr,
    "1 day",                                    # barSizeSetting,
    "TRADES",                                   # whatToShow,
    0,                                          # useRTH,
    1,                                          # formatDate
    None                                        # chartOptions
)

print("\n====================================================================")
print(" History requested, waiting %ds for TWS responses" % WAIT_TIME)
print("====================================================================\n")


try:
    callback.got_history.wait(timeout=WAIT_TIME)
except KeyboardInterrupt:
    pass
finally:
    if not callback.got_history.is_set():
        print('Failed to get history within %d seconds' % WAIT_TIME)

    print("\nDisconnecting...")
    tws.eDisconnect()
