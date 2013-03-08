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

from swigibpy import EWrapper, EPosixClientSocket, Contract

try:
    input = raw_input
except:
    pass

###


class HistoricalDataExample(EWrapper):
    '''Callback object passed to TWS, these functions will be called directly
    by TWS.

    '''

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
        else:
            date = datetime.strptime(date, "%Y%m%d").strftime("%d %b %Y")
            print(("History %s - Open: %s, High: %s, Low: %s, Close: " +
                    "%s, Volume: %d") % (date, open, high, low, close, volume))


# Instantiate our callback object
callback = HistoricalDataExample()

# Instantiate a socket object, allowing us to call TWS directly. Pass our
# callback object so TWS can respond.
tws = EPosixClientSocket(callback)

# Connect to tws running on localhost
tws.eConnect("", 7496, 42)

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
        1                                           # formatDate
    )

print("\n=====================================================================")
print(" History requested, waiting for TWS responses")
print("=====================================================================\n")


print("******************* Press ENTER to quit when done *******************\n")
input()

print("\nDisconnecting...")
tws.eDisconnect()
