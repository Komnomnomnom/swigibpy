'''Simple example of using the SWIG generated TWS wrapper to place an order
with interactive brokers.

'''

import sys
from threading import Event

from swigibpy import (EWrapper, EPosixClientSocket, Contract, Order, TagValue,
                      TagValueList)


WAIT_TIME = 10.0


try:
    # Python 2 compatibility
    input = raw_input
    from Queue import Queue
except:
    from queue import Queue

###


class PlaceOrderExample(EWrapper):
    '''Callback object passed to TWS, these functions will be called directly
    by TWS.

    '''

    def __init__(self):
        super(PlaceOrderExample, self).__init__()
        self.order_filled = Event()
        self.order_ids = Queue()

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
        self.order_ids.put(validOrderId)

    def orderStatus(self, id, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFilledPrice, clientId, whyHeld):

        print(("Order #%s - %s (filled %d, remaining %d, avgFillPrice %f,"
               "last fill price %f)") %
              (id, status, filled, remaining, avgFillPrice, lastFilledPrice))
        if remaining <= 0:
            self.order_filled.set()

    def openOrder(self, orderID, contract, order, orderState):

        print("Order opened for %s" % contract.symbol)

    def commissionReport(self, commissionReport):
        print 'Commission %s %s P&L: %s' % (commissionReport.currency,
                                            commissionReport.commission,
                                            commissionReport.realizedPNL)

prompt = input("WARNING: This example will place an order on your IB "
               "account, are you sure? (Type yes to continue): ")
if prompt.lower() != 'yes':
    sys.exit()

# Instantiate our callback object
callback = PlaceOrderExample()

# Instantiate a socket object, allowing us to call TWS directly. Pass our
# callback object so TWS can respond.
tws = EPosixClientSocket(callback)

# Connect to tws running on localhost
if not tws.eConnect("", 7496, 42):
    raise RuntimeError('Failed to connect to TWS')

# Simple contract for GOOG
contract = Contract()
contract.symbol = "IBM"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

print('Waiting for valid order id')
order_id = callback.order_ids.get(timeout=WAIT_TIME)
if not order_id:
    raise RuntimeError('Failed to receive order id after %ds' % WAIT_TIME)

# Order details
algoParams = TagValueList()
algoParams.append(TagValue("componentSize", "3"))
algoParams.append(TagValue("timeBetweenOrders", "60"))
algoParams.append(TagValue("randomizeTime20", "1"))
algoParams.append(TagValue("randomizeSize55", "1"))
algoParams.append(TagValue("giveUp", "1"))
algoParams.append(TagValue("catchUp", "1"))
algoParams.append(TagValue("waitForFill", "1"))
algoParams.append(TagValue("startTime", "20110302-14:30:00 GMT"))
algoParams.append(TagValue("endTime", "20110302-21:00:00 GMT"))

order = Order()
order.action = 'BUY'
order.lmtPrice = 140
order.orderType = 'LMT'
order.totalQuantity = 10
order.algoStrategy = "AD"
order.tif = 'DAT'
order.algoParams = algoParams
#order.transmit = False


print("Placing order for %d %s's (id: %d)" % (order.totalQuantity,
                                              contract.symbol, order_id))

# Place the order
tws.placeOrder(
    order_id,                                   # orderId,
    contract,                                   # contract,
    order                                       # order
)

print("\n====================================================================")
print(" Order placed, waiting %ds for TWS responses" % WAIT_TIME)
print("====================================================================\n")


print("Waiting for order to be filled..")

try:
    callback.order_filled.wait(WAIT_TIME)
except KeyboardInterrupt:
    pass
finally:
    if not callback.order_filled.is_set():
        print('Failed to fill order')

    print("\nDisconnecting...")
    tws.eDisconnect()
