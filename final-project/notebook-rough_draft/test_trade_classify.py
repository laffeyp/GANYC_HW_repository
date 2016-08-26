from cbe import CoinbaseExchange
import json
import numpy as np
import pandas as pd
import time as timer
from datetime import datetime
from dateutil.relativedelta import *
from sklearn.externals import joblib
model = joblib.load('sgd_simple.pkl')
# simple and naive algorithm that assumes you start with one btc and
# must then sell high and buy low in order to profit.
cb = CoinbaseExchange()



price = []
time = []
prediction = 0.0
starttime=timer.time()
buy = False
sell = False
hold = False
bought_at = 0
sold_at = 0
profit = 0
total_profit = 0
sell_price = 0
num_buy = 0
num_sell = 0

# depends on the last 360 ten second ticks, so we need to get that data
# so we don't have to wait an hour.
now = datetime.now()
end = now - relativedelta(seconds=-4000)
json_historic = cb.getProductHistoricRates(now, end, 10)
print "help"
#carefull how we handle overlap here
while len(json_historic) < 361:
    now = now - relativedelta(seconds=-4000)
    end = end - relativedelta(seconds=-4000)
    ret = cb.getProductHistoricRates(now, end, 10)
    json_historic += ret
print json_historic
print "help"
price = []
for elem in json_historic:
    #historic_time.append(elem[0])
    #historic_low.append(elem[1])
    #historic_high.append(elem[2])
    #historic_open.append(elem[3])
    price.append(float(elem[4]))
    #historic_volume.append(elem[5])

print len(price)

while len(price)>361:
    price.pop(0)

price.reverse()
while True:

    # as soon as we have enough prices.
    price_in = np.array([price])
    price_in = np.diff(price_in)
    price_in = price_in[~np.isnan(price_in)]
    print price_in
    price_in.reshape(-1,1)
    print np.shape(price_in)
    prediction = model.predict(price_in) 
    print prediction
    #need to reverse array? how does model take in data?



    if (prediction == 1) and (num_buy <= num_sell):

        print "buy at %f " % price[360], prediction
        buy = True
        sell = False
        hold = False
        num_buy += 1
        bought_at = price[360]



    if (prediction == 0 ) and (num_sell < num_buy):

        print "sell at %f" % price[360], prediction
        buy = False
        sell = True
        hold = False
        num_sell += 1
        sold_at = price[360]
        profit = sold_at - bought_at
        total_profit += profit
        print profit
        print total_profit




    timer.sleep(10.0 - ((timer.time() - starttime) % 10.0))
    json_ticker = cb.getProductTicker()
    actual = float(json_ticker['price'])
    #print type(actual)
    price.append(actual)
    price.pop(0)


# this whole thing will need to be modified for classification - up or down
#is also not too useful, really, on a ten second basis. needs to be up or down
# by a certain amount.

# could possibly chain together different methods??

# get enough prices to make prediction, then keep making predictions,
#how does this work????
# if predicted price is x higher than current price, buy, if x lower than current
#price, sell, else do nothing??
# will need to write own classes etc.
# also if you are only allowed a very small amount to trade with,
# you need to sell if the last was buy or do nothing, and vice versa
