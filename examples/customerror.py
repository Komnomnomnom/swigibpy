'''Simple example of using custom error hanlding with the SWIG generated TWS 
wrapper.

Check http://www.interactivebrokers.com/en/software/api/api.htm -> 'Reference 
Tables' -> 'API Message Codes' for error codes and their interpretation.

'''

import sys
from datetime import datetime

from swigibpy import EWrapper, EPosixClientSocket, Contract
from swigibpy import TWSError, TWSClientError, TWSSystemError, TWSWarning

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
        try:
            super(CustomErrorExample, self).error(id, errCode, errString)
        except TWSWarning as w:
            print("TWS warns %s" % w.msg)
        except TWSClientError as c:
            if c.code == 502:
                print('Looks like TWS is not running, '
                      'start it up and try again')
                sys.exit()
            else:
                print("TWS reports error in client: %s" % c.msg)
        except TWSSystemError as s:
            print("TWS reports system error: %s" % s.msg)
        except TWSError as e:
            print("TWS reports error: %s" % e.msg)

    def winError(self, msg, lastError):
        try:
            super(CustomErrorExample, self).winError(msg, lastError)
        except TWSClientError as c:
            print("TWS reports API error: %s" % c.msg)


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
