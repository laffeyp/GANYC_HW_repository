Alot of material you've got in terms of showing various movements and relationships in data, but tough to follow along to the untrained eye. While you do have comments in your code, a more polished and probably more useful thing to do would be to insert some nice explanatory text via markdown cells.

Also, from what we talked about in class, this might reduce the lines of code and time you’re using to do your lagged time series.

[pandas.pct_change()](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.pct_change.html)

The pct_change() function of a pandas data frame or a pandas series has a parameter called “periods” which you can change to get the % change in prices for different time periods. Given your data was grouped into data by the minute, you might have to calculate some arbitrarily large “periods” to designate a ‘day’, ‘week’, or ‘month.
