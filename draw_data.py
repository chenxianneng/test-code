import matplotlib.pyplot as plt
import seaborn as sns
# import seaborn.linearmodels as snsl

from datetime import datetime
import tushare as ts

sns.set_style("whitegrid")
end = datetime.today() #开始时间结束时间，选取最近一年的数据
start = datetime(end.year-5,end.month,end.day)
end = str(end)[0:10]
start = str(start)[0:10]

stock = ts.get_hist_data('601985',start,end)#选取一支股票
stock['close'].plot(legend=True ,figsize=(10,4))
plt.show()