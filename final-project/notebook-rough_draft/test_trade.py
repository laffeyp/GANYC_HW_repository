#naive program to test model
from cbe import CoinbaseExchange
import json
import numpy as np
import pandas as pd
import time as timer
from sklearn.externals import joblib
model = joblib.load('brr_simple.pkl')

cb = CoinbaseExchange()

json_ticker = cb.getProductTicker()

price = []
time = []
prediction = 0.0
starttime=timer.time()
buy = False
sell = False
hold = False
profit = 0
total_profit = 0
sell_price = 0
num_buy = 1
num_sell = 0

#this will need to be own subprocess or method
while True:
    json_ticker = cb.getProductTicker()
    actual = float(json_ticker['price'])

    if sell == True:
        profit = sell_price - actual
        total_profit += sell_price - actual
        print "total profit: %f, profit %f" %(total_profit, profit)

    price.append(actual)
    #time.append(str(json_ticker['time']))

    print price
    # need way to tell what prev trade was...
    if len(price) == 5:
        price_in = np.asarray([price])
        price_in.reshape(-1,1)
        prediction = model.predict(price_in) # need to round

        #need to set if else windows less than price + x but less than price + y etc

        if (prediction > (price[4] + .01)) and (num_buy <= num_sell):

                print "buy at %f predicted is %f" % (price[4], prediction)
                buy = True
                sell = False
                hold = False
                num_buy += 1


        if (prediction < (price[4] - .01 )) and (num_sell > num_buy):

                print "sell at %f, predicted is %f" % (price[4], prediction)
                sell_price = price[4]
                buy = False
                sell = True
                hold = False
                num_sell += 1


        elif prediction >= (price[4] - .01 ) and prediction <= (price[4] + .01 ) :
            print "hold at %f predicted is %f" % (price[4], prediction)
            #buy = False
            #sell = False
            hold = True



        #time = []
        price.pop(0)
    timer.sleep(60.0 - ((timer.time() - starttime) % 60.0))
# get enough prices to make prediction, then keep making predictions,
#how does this work????
# if predicted price is x higher than current price, buy, if x lower than current
#price, sell, else do nothing??
# will need to write own classes etc.
# also if you are only allowed a very small amount to trade with,
# you need to sell if the last was buy or do nothing, and vice versa
