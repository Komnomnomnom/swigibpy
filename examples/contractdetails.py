'''Simple example of requesting using the SWIG generated TWS wrapper to
request contract details from Interactive Brokers.

'''

from datetime import datetime

from swigibpy import EWrapper, EPosixClientSocket, Contract

try:
    input = raw_input
except:
    pass

###


class ContractDetailsExample(EWrapper):
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

    def contractDetailsEnd(self, reqId):
        print("Contract details request complete, (request id %i)" % reqId)

    def contractDetails(self, reqId, contractDetails):
        print("Contract details received (request id %i):" % reqId)
        print("callable: %s" % contractDetails.callable)
        print("category: %s" % contractDetails.category)
        print("contractMonth: %s" % contractDetails.contractMonth)
        print("convertible: %s" % contractDetails.convertible)
        print("coupon: %s" % contractDetails.coupon)
        print("industry: %s" % contractDetails.industry)
        print("liquidHours: %s" % contractDetails.liquidHours)
        print("longName: %s" % contractDetails.longName)
        print("marketName: %s" % contractDetails.marketName)
        print("minTick: %s" % contractDetails.minTick)
        print("nextOptionPartial: %s" % contractDetails.nextOptionPartial)
        print("orderTypes: %s" % contractDetails.orderTypes)
        print("priceMagnifier: %s" % contractDetails.priceMagnifier)
        print("putable: %s" % contractDetails.putable)
        if contractDetails.secIdList is not None:
            for secId in contractDetails.secIdList:
                print("secIdList: %s" % secId)
        else:
            print("secIdList: None")

        print("subcategory: %s" % contractDetails.subcategory)
        print("tradingClass: %s" % contractDetails.tradingClass)
        print("tradingHours: %s" % contractDetails.tradingHours)
        print("timeZoneId: %s" % contractDetails.timeZoneId)
        print("underConId: %s" % contractDetails.underConId)
        print("evRule: %s" % contractDetails.evRule)
        print("evMultiplier: %s" % contractDetails.evMultiplier)

        contract = contractDetails.summary

        print("\nContract Summary:")
        print("exchange: %s" % contract.exchange)
        print("symbol: %s" % contract.symbol)
        print("secType: %s" % contract.secType)
        print("currency: %s" % contract.currency)
        if contract.comboLegs is not None:
            for comboLeg in contract.comboLegs:
                print("comboLegs: %s - %s" % (comboLeg.action, comboLeg.exchange))
        else:
            print("comboLegs: None")

        print("\nBond Values:")
        print("bondType: %s" % contractDetails.bondType)
        print("couponType: %s" % contractDetails.couponType)
        print("cusip: %s" % contractDetails.cusip)
        print("descAppend: %s" % contractDetails.descAppend)
        print("issueDate: %s" % contractDetails.issueDate)
        print("maturity: %s" % contractDetails.maturity)
        print("nextOptionDate: %s" % contractDetails.nextOptionDate)
        print("nextOptionType: %s" % contractDetails.nextOptionType)
        print("notes: %s" % contractDetails.notes)
        print("ratings: %s" % contractDetails.ratings)
        print("validExchanges: %s" % contractDetails.validExchanges)


# Instantiate our callback object
callback = ContractDetailsExample()

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

print("Requesting contract details...")

# Perform the request
tws.reqContractDetails(
        42,                                         # reqId,
        contract,                                   # contract,
    )

print("\n=====================================================================")
print(" Contract details requested, waiting for TWS responses")
print("=====================================================================\n")


print("******************* Press ENTER to quit when done *******************\n")
input()

print("\nDisconnecting...")
tws.eDisconnect()
