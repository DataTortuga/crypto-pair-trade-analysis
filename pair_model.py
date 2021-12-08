# Import data science essentials
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import copy
from numpy import matlib
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.tsa.stattools as ts

# Import plotting essentials
#import matplotlib.pyplot as plt

# from Config.api_key import coin_key


# Put API data into a csv files so I wouldn't have to call it all the time.

# from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# import json

# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical'
# parameters = {
#   'id':'1,1027',
#   'time_start':'2021-09-10',
#   'time_end': '2021-10-09',
#   'convert':'USD'
# }
# headers = {
#   'Accepts': 'application/json',
#   'X-CMC_PRO_API_KEY': coin_key,
# }

# session = Session()
# session.headers.update(headers)

# try:
#   response = session.get(url, params=parameters)
#   data = json.loads(response.text)
#   json_formatted_str = json.dumps(data, indent=2)
#   print(json_formatted_str)
# except (ConnectionError, Timeout, TooManyRedirects) as e:
#   print(e)


def model(lookback):
        
    btc_file = "BTC-ETH-Pair-Trade/api_btc.csv"
    eth_file = "BTC-ETH-Pair-Trade/api_eth.csv"

    btc_df = pd.read_csv(btc_file)
    eth_df = pd.read_csv(eth_file)

    spread_btc = btc_df
    spread_eth = eth_df


    # Were finally ready to start implementing the pair trade model! 

    # First set an arbitrary lookback window and introduce bias into the model. Ideally we should use a quantitative
    # method to approximate this, but again no time. Ornstein–Uhlenbeck formula is a good choice to estimate half-life
    # of mean reversion, however again, no time.

    # Possibly could use a Data Science approach like a grid search or something and filter results for highest returns
    # but thats a fantastic way to introduce over-fitting. I personally find quantitative approaches more comforting.
    lookback=lookback

    # Pre-allocate hedgeRatio array
    hedgeRatio=np.empty(len(spread_btc))
    hedgeRatio[:]=np.nan

    # Use for loop, lookback window, and OLS to estimate hedgeRatio (BTC-hedgeRatio*ETH)
    for t in range(lookback,len(hedgeRatio),1):
        
        regression_result=sm.OLS(spread_btc[t-lookback:t],spread_eth[t-lookback:t]).fit()
        hedgeRatio[t]=regression_result.params[0]


    # y2 = [independent_spread dependent_spread]

    # Create array to store prices for ETH and BTC
    y2 = np.array([spread_eth, spread_btc]).transpose()

    # introducing massive amounts of look-ahead bias :)
    hedgeRatio_df = pd.DataFrame(hedgeRatio,columns=['Hedge Ratio'])
    hedgeRatio_df.fillna(method='bfill',inplace=True)
    hedgeRatio_df['Ones'] = np.ones(len(spread_btc))
    hedgeRatio1 = copy.deepcopy(hedgeRatio_df)


    # For next step we need the negative of the hedgeRatio so...
    hedgeRatio1['Hedge Ratio'] = hedgeRatio1['Hedge Ratio']*-1.0


    # Calculating unit portfolio price using hedgeRatio and ETH-BTC prices
    yport = np.sum(np.multiply(hedgeRatio1,y2[0]),axis=1)



    # Convert unit portfolio to df
    yport_df = pd.DataFrame(yport)



    # For Linear Mean Reversion strategy we scale into the position as the unit portfolio
    # deviates further from its mean. Anticipating mean reversion we unload the position and capture a profit....
    # at least theoretically.
    zScore=-(yport_df-yport_df.rolling(window=lookback).mean())/yport_df.rolling(window=lookback).std()

    # This backfill introduces look-ahead bias but I had to deal with the nan somehow. In a production model this
    # is certainly a no no.
    zScore.fillna(method='bfill',inplace=True)


    # Had to create a deep copy since y2 is overwritten when calculating positions. IDK why that happens though.
    y3 = copy.deepcopy(y2[0])


    hedgeRatio2 = copy.deepcopy(hedgeRatio_df)
    # Preparing hedgeRatio df for calculating daily position sizes in next cell
    hedgeRatio2['Ones'] = hedgeRatio2['Ones']*-1.0

    # Positions array for Linear Mean Reversion Strategy
    positions = np.multiply(matlib.repmat(zScore,1,2),hedgeRatio2,y2[0])


    # Calculating Daily Profit and Loss
    # This is as simple as multiplying the position size times the calculated returns using y3

    pnl_arr = [0]
        
    for i in range(1,y3.shape[0]):
        
        # Calculate pnl for independent variable (ETH)
        independent_return = positions[i-1,0]*((y3[i,0]-y3[i-1,0])/y3[i-1,0])
        
        # Calcualate pnl for dependent variable (BTC)
        dependent_return = positions[i-1,1]*(y3[i,1]-y3[i-1,1])/y3[i-1,1]
        
        # Compute daily_pnl by summing pnl for independent and dependent variable
        daily_pnl = independent_return+dependent_return
            
        pnl_arr.append(daily_pnl)

    pnl_df = pd.DataFrame(pnl_arr,columns=['Daily PnL'])
    positions_df = pd.DataFrame(positions,columns=['ETH Position','BTC Position'])


    # temp_df is calculating the gross market value of the portfolio in preparation for returns in next cell
    temp_df = positions_df.shift(1).abs().sum(axis=1)


    # Computing daily returns
    ret_df = pnl_df['Daily PnL'].div(temp_df)

    # Computing cumulative returns. I'm so glad pandas has functions built in for this!
    cumulative_ret = ret_df[1:].add(1).cumprod().sub(1)

    return cumulative_ret

# # Plotting cumulative returns
# plt.plot(cumulative_ret,label='Strategy Cumulative Returns')
# plt.xlabel('Days')
# plt.ylabel('Cumulative Returns')
# plt.grid()
# plt.legend()
# plt.show()