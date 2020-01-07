import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS
from quantopian.pipeline.factors import SimpleMovingAverage
import talib



def initialize(context):
    context.securities = symbols('AAPL','MSFT','IBM','TSLA','AMZN')
    context.period=14
    #the 0.99 ensures that the weights sum up to 1
    context.weights = 0.99/len(context.securities) 
    set_benchmark(sid(24))
    context.low_RSI = 30
    context.high_RSI = 60
    for minute in range(1, 386, 60): # steps by 60 mins
        schedule_function(rebalance, date_rules.every_day(), time_rules.market_open(minutes=minute))
    
    
def rebalance(context, data):
    for stock in context.securities:
        H = data.history(stock, 'high', context.period + 1, '1d') 
        L = data.history(stock, 'low', context.period + 1, '1d') 
        price_hist1 = data.history(stock, 'price', 5, '1d')  
        m5 = price_hist1.mean()  
        price_hist2 = data.history(stock, 'price', 20, '1d')  
        m20 = price_hist2.mean() 
        prices = data.history(stock, 'price', 40, '1d')
        rsi = talib.RSI(prices, timeperiod=14)[-1]
        AroonDown, AroonUp = talib.AROON(H, L, context.period) 
        Aroon_dif = AroonUp[-1] - AroonDown[-1]
        current_positions = context.portfolio.positions[stock].amount
        #print("%s %s" % (current_positions, stock))
        #cash = context.portfolio.cash
        #buying condition
        if (m5 > m20) and current_positions == 0:
          order_target_percent(stock, context.weights)
          print('Buying shares ' + str(stock))
          print(Aroon_dif)
    #selling condtion
        elif (m5 < m20) and current_positions != 0 and rsi > context.high_RSI:
          order_target_percent(stock, 0)
          print('Selling shares' + str(stock))