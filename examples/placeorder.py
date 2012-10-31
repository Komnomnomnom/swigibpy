'''Simple example of using the SWIG generated TWS wrapper to place an order
with interactive brokers.

'''

import sys
from time import sleep

from swigibpy import EWrapper, EPosixClientSocket, Contract, Order

###

orderId = None


class PlaceOrderExample(EWrapper):
    '''Callback object passed to TWS, these functions will be called directly
    by TWS.

    '''

    def openOrderEnd(self):
        '''Not relevant for our example'''
        pass

    def execDetails(self, id, contract, execution):
        '''Not relevant for our example'''
        pass

    def managedAccounts(self, openOrderEnd):
        '''Not relevant for our example'''
        pass

    ###############

    def nextValidId(self, validOrderId):
        '''Capture the next order id'''
        global orderId
        orderId = validOrderId

    def orderStatus(self, id, status, filled, remaining, avgFillPrice, permId,
            parentId, lastFilledPrice, clientId, whyHeld):

        print ("Order #%s - %s (filled %d, remaining %d, avgFillPrice %f,"
               "last fill price %f)") % (
                id, status, filled, remaining, avgFillPrice, lastFilledPrice)

    def openOrder(self, orderID, contract, order, orderState):

        print "Order opened for %s" % contract.symbol

prompt = raw_input("WARNING: This example will place an order on your IB "
                   "account, are you sure? (Type yes to continue): ")
if prompt.lower() != 'yes':
    sys.exit()

# Instantiate our callback object
callback = PlaceOrderExample()

# Instantiate a socket object, allowing us to call TWS directly. Pass our
# callback object so TWS can respond.
tws = EPosixClientSocket(callback)

# Connect to tws running on localhost
tws.eConnect("", 7496, 42)

# Simple contract for GOOG
contract = Contract()
contract.exchange = "SMART"
contract.symbol = "DELL"
contract.secType = "STK"
contract.currency = "USD"

if orderId is None:
    print 'Waiting for valid order id'
    sleep(1)
    while orderId is None:
        print 'Still waiting for valid order id...'
        sleep(1)

# Order details
order = Order()
order.action = 'BUY'
order.lmtPrice = 0
order.auxPrice = 0
order.orderType = 'MTL'
order.totalQuantity = 1


print "Placing order for %d %s's (id: %d)" % (order.totalQuantity,
        contract.symbol, orderId)

# Place the order
tws.placeOrder(
        orderId,                                    # orderId,
        contract,                                   # contract,
        order                                       # order
    )

print "\n====================================================================="
print " Order placed, waiting for TWS responses"
print "=====================================================================\n"


print "******************* Press ENTER to quit when done *******************\n"
raw_input()

print "\nDisconnecting..."
tws.eDisconnect()
