# Description: Find the distribution of last digit of stock close price
# Author: Haotian Zhu
# Date: Apr 10, 2019

import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# here I replaced my actual token with "mytoken"
ts.set_token("mytoken") 
# init tushare api
pro = ts.pro_api()

# get all stock code
stock_info = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code')
stock_info_arr = stock_info["ts_code"].unique()

# init empty dataframe
result = pd.DataFrame()
for (index, stock_code) in enumerate(stock_info_arr):
    # print current stock info
    print(index, "Processing", stock_code)
    while(True):
        try:
            # load stock data from 2014-01-01
            stock_data = pro.daily(ts_code=stock_code, start_date='20140101')
        except(ConnectionError, Exception):
            # pause to avoid connecting api too frequently
            time.sleep(60) 
            continue
        break
    # get the unit digit of stock
    unit_digit = stock_data['close'].astype("int") %10 
    # count frequency
    unit_digit_count = unit_digit.value_counts().to_frame()
    # add new result with previous result
    result = result.add(unit_digit_count, fill_value=0)

result.plot.bar()
