#!/usr/bin/python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
# import seaborn.linearmodels as snsl

from datetime import datetime
import tushare as ts

import pandas as pd  
import numpy as np
#正常显示画图时出现的中文
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
stocks={'中国平安':'601318', '格力电器':'000651', '招商银行':'600036', '恒生电子':'600570', '中信证券':'600030', '贵州茅台':'600519'}
startdate='2018-01-01'

#构建一个计算股票收益率和标准差的函数
#默认起始时间为'2005-01-01'
def return_risk(stocks,startdate='2017-01-01'):
    close=pd.DataFrame()
    for stock in stocks.values():
        close[stock] = ts.get_k_data(stock, ktype='D', autype='qfq', start = startdate)['close']
        # print(stock, close[stock])

    tech_rets = close.pct_change()[1:]
    rets = tech_rets.dropna()
    ret_mean=rets.mean()*100
    ret_std=rets.std()*100
    return ret_mean,ret_std

#画图函数
def plot_return_risk():
    ret,vol=return_risk(stocks)
    color=np.array([ 0.18, 0.96, 0.75, 0.3, 0.9,0.5])
    plt.scatter(ret, vol, marker = 'o', c=color,s = 500,cmap=plt.get_cmap('Spectral'))
    plt.xlabel("日收益率均值%")     
    plt.ylabel("标准差%")

    for label,x,y in zip(stocks.keys(),ret,vol):
        plt.annotate(label,xy = (x,y),xytext = (20,20),
        textcoords = "offset points",
        ha = "right",va = "bottom",
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = "->",connectionstyle = "arc3,rad=0"))

    plt.show()

# stocks={'上证指数':'sh','深证指数':'sz','沪深300':'hs300',
#  '上证50':'sz50','中小板指数':'zxb','创业板指数':'cyb'}

# plot_return_risk()

plot_return_risk()