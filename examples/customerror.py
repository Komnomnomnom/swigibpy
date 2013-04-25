'''Simple example of using custom error hanlding with the SWIG generated TWS 
wrapper.

Check http://www.interactivebrokers.com/en/software/api/api.htm -> 'Reference 
Tables' -> 'API Message Codes' for error codes and their interpretation.

'''

import sys
from datetime import datetime

from swigibpy import EWrapper, EPosixClientSocket, Contract

try:
    input = raw_input
except:
    pass

###


class CustomErrorExample(EWrapper):
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

        pass

    def error(self, id, errCode, errString):

        if errCode == 165 or (errCode >= 2100 and errCode <= 2110):
            print("TWS warns %s" % errString)
        elif errCode == 502:
            print('Looks like TWS is not running, '
                  'start it up and try again')
            sys.exit()
        elif errCode == 501:
            print("TWS reports error in client: %s" % errString)
        elif errCode >= 1100 and errCode < 2100:
            print("TWS reports system error: %s" % errString)
        elif errCode == 321:
            print("TWS complaining about bad request: %s" % errString)
        else:
            super(CustomErrorExample, self).error(id, errCode, errString)

    def winError(self, msg, lastError):
        print("TWS reports API error: %s" % msg)


# Instantiate our callback object
callback = CustomErrorExample()

# Instantiate a socket object, allowing us to call TWS directly. Pass our
# callback object so TWS can respond.
tws = EPosixClientSocket(callback)

# Connect to tws running on localhost
tws.eConnect("", 7496, 42)

# Simple (badly formed) contract
contract = Contract()
contract.exchange = "SMART"
contract.secType = "STK"
today = datetime.today()

print("Sending bad request for historical data")

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
print(" Waiting for TWS responses")
print("=====================================================================\n")


print("******************* Press ENTER to quit when done *******************\n")
input()

print("\nDisconnecting...")
tws.eDisconnect()
