import quandl
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, date2num, WeekdayLocator, DayLocator, MONDAY


# Using ggplot style for plots

plt.style.use('ggplot')

# Setting Quandl API key

quandl.ApiConfig.api_key = "yL7SLkU2_56dp7gGChJy"

# Obtaining the historical stock information for Tesla, Ford, GM
# from Jan 1, 2012 to Jan 1, 2017 using Quandl.

start = datetime(2012, 1, 1)
end = datetime(2017, 1, 1)

tesla = quandl.get("WIKI/TSLA", start_date=start, end_date=end)
ford = quandl.get("WIKI/F", start_date=start, end_date=end)
gm = quandl.get("WIKI/GM", start_date=start, end_date=end)

# Linear plot of all the stock's Open price

tesla["Open"].plot(label="Tesla", figsize=(12,8), title='Opening Prices')
gm["Open"].plot(label="GM")
ford["Open"].plot(label="Ford")
plt.legend()

# Showing the date of rhe maximum trading volume for Ford

ford["Volume"].argmax()

# Creating a new column for each dataframe called "Total Traded"
# which is the Open Price multiplied by the Volume Traded.

tesla["Total Traded"] = tesla['Open'] * tesla['Volume']
ford["Total Traded"] = ford['Open'] * ford['Volume']
gm["Total Traded"] = gm['Open'] * gm['Volume']

# Plotting the "Total Traded" against the time index.

tesla["Total Traded"].plot(label="Tesla", figsize=(16,8))
ford["Total Traded"].plot(label="Ford")
gm["Total Traded"].plot(label="GM")
plt.legend()

# Creating and plotting Moving Averages(MA50 and MA200)

tesla["MA50"] = tesla['Open'].rolling(50).mean()
tesla["MA200"] = tesla['Open'].rolling(200).mean()

tesla[['Open', 'MA50', 'MA200']].plot(figsize=(16,8))

# Checking if there is a relationship between these stocks using
# a scatter matrix plot. Rearranging the Open columns into a new dataframe.

car_comp = pd.concat([tesla['Open'], gm['Open'], ford['Open']], axis=1)
car_comp.columns = ['Tesla Open', 'GM Open', 'Ford Open']
scatter_matrix(car_comp, figsize=(8,8), alpha=0.2, hist_kwds={'bins': 50})

# Creating a candlestick chart for Ford in January 2012

ford_reset = ford.loc['2012-01'].reset_index()
ford_reset['date_ax'] = ford_reset['Date'].apply(lambda date: date2num(date))
list_of_cols = ['date_ax', 'Open', 'High', 'Low', 'Close']
ford_values = [tuple(vals) for vals in ford_reset[list_of_cols].values]

mondays = WeekdayLocator(MONDAY)
alldays = DayLocator()
weekFormatter = DateFormatter('%b %d')
dayFormatter = DateFormatter('%d')

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)
#ax.xaxis.set_minor_formatter(dayFormatter)

candlestick_ohlc(ax,ford_values,width=0.6,colorup='g',colordown='r')

# Calculating daily percentage change

tesla['returns'] = (tesla['Close'] / tesla['Close'].shift(1)) - 1

# Or

gm['returns'] = gm['Close'].pct_change(1)
ford['returns'] = ford['Close'].pct_change(1)

# Plotting a histograms stacking them on top of each other to show
# which stock is the most “volatile”

tesla['returns'].hist(bins=100,label="Tesla",figsize=(10,8),alpha=0.4)
gm['returns'].hist(bins=100,label="GM",figsize=(10,8),alpha=0.4)
ford['returns'].hist(bins=100,label="Ford",figsize=(10,8),alpha=0.4)
plt.legend()

# Plotting a kernel density estimation for another point of view.

tesla['returns'].plot(kind='kde',label='Tesla',figsize=(10,8))
gm['returns'].plot(kind='kde',label='GM',figsize=(10,8))
ford['returns'].plot(kind='kde',label='Ford',figsize=(10,8))
plt.legend()

# Creating box plots comparing the returns.

box_df = pd.concat([tesla['returns'],ford['returns'],gm['returns']], axis=1)
box_df.columns = ['Tesla Returns','Ford Returns','GM Returns']
box_df.plot(kind='box',figsize=(8,11))

# Create a scatter matrix plot to see the correlation between each of the
# stocks daily returns.

scatter_matrix(box_df,figsize=(8,8),alpha=0.2,hist_kwds={'bins':100})

# Creating a cumulative daily return column for each car company's dataframe.
# Comparing current day return to the very first day.

tesla['Cumulative Return'] = (1 + tesla['returns']).cumprod()
gm['Cumulative Return'] = (1 + gm['returns']).cumprod()
ford['Cumulative Return'] = (1 + ford['returns']).cumprod()

plt.clf()

# Plotting the Cumulative Return columns against the time series index to
# find out which stock showed the highest return for a $1 invested, the lowest

tesla["Cumulative Return"].plot(label='Tesla',figsize=(16,8))
ford["Cumulative Return"].plot(label='Ford')
gm["Cumulative Return"].plot(label='GM')
plt.legend()
