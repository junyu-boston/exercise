# 1. Select index components & import data
### A. Explore and clean company listing information

# Inspect listings
print(listings.info())

# Move 'stock symbol' into the index
listings.set_index('Stock Symbol', inplace=True)

# Drop rows with missing 'sector' data
listings.dropna(subset=['Sector'], inplace=True)

# Select companies with IPO Year before 2019
listings = listings[listings['IPO Year']<2019]

# Inspect the new listings data
print(listings.info())

# Show the number of companies per sector
print(listings.groupby('Sector').size().sort_values(ascending=False))


### B. Select and inspect index components

In [1]:
listings.head()
Out[1]:

             Exchange                  Company Name  Last Sale  Market Capitalization  IPO Year                 Sector                             Industry
Stock Symbol                                                                                                                                               
ACU              amex      Acme United Corporation.      27.39                  91.14  1,988.00          Capital Goods      Industrial Machinery/Components
ROX              amex           Castle Brands, Inc.       1.46                 237.64  2,006.00  Consumer Non-Durables  Beverages (Production/Distribution)
CQP              amex  Cheniere Energy Partners, LP      32.70              11,046.92  2,007.00       Public Utilities                 Oil/Gas Transmission
CIX              amex      CompX International Inc.      14.35                 178.21  1,998.00          Capital Goods      Industrial Machinery/Components
GSAT             amex              Globalstar, Inc.       1.73               1,931.55  2,006.00      Consumer Services         Telecommunications Equipment
In [2]:
listings.info()
<class 'pandas.core.frame.DataFrame'>
Index: 1015 entries, ACU to YPF
Data columns (total 7 columns):
Exchange                 1015 non-null object
Company Name             1015 non-null object
Last Sale                1015 non-null float64
Market Capitalization    1015 non-null float64
IPO Year                 1015 non-null float64
Sector                   1015 non-null object
Industry                 1015 non-null object
dtypes: float64(3), object(4)
memory usage: 103.4+ KB
 
# Select largest company for each sector
components = listings.groupby('Sector')['Market Capitalization'].nlargest(1)

# Print components, sorted by market cap
print(components.sort_values(ascending=False))

# Select stock symbols and print the result
tickers = components.index.get_level_values('Stock Symbol')
print(tickers)

# Print company name, market cap, and last price for each component 
info_cols = ['Company Name', 'Market Capitalization', 'Last Sale']
print(listings.loc[tickers, info_cols].sort_values('Market Capitalization', ascending=False))

### C. Import index component price information
# Print tickers
print(tickers)

# Import prices and inspect result
stock_prices = pd.read_csv('stock_prices.csv', parse_dates=['Date'], index_col='Date')
print(stock_prices.info())

# Calculate the returns
price_return = stock_prices.iloc[-1,:].div(stock_prices.iloc[0, :]).sub(1).mul(100)

# Plot horizontal bar chart of sorted price_return   
price_return.sort_values().plot(kind='barh')
plt.title('Stock Price Returns')
plt.show()

# 2. Build a market-cap weighted index
# Select components and relevant columns from listings
components = listings.loc[tickers, ['Market Capitalization', 'Last Sale']]

# Print the first rows of components
print(components.head())

# Calculate the number of shares here
no_shares = components['Market Capitalization'].div(components['Last Sale'])

# Print the sorted no_shares
print(no_shares.sort_values(ascending=False))

# Select the number of shares
no_shares = components['Number of Shares']
print(no_shares.sort_values())

# Create the series of market cap per ticker
market_cap = stock_prices.mul(no_shares)

# Select first and last market cap here
first_value = market_cap.iloc[0]
last_value = market_cap.iloc[-1]


# Concatenate and plot first and last market cap here

pd.concat([first_value, last_value], axis=1).plot(kind='barh')
plt.show()

### Calculate & plot the composite index
# Aggregate and print the market cap per trading day
raw_index = market_cap_series.sum(axis=1)
print(raw_index)

# Normalize the aggregate market cap here 
index = raw_index.div(raw_index.iloc[0]).mul(100)
print(index)

# Plot the index here
index.plot(title='Market_Cap Weighted Index')
plt.show()

### Evaluate Index Performance
# Calculate and print the index return here
index_return = (index.iloc[-1]/index.iloc[0]-1)* 100
print(index_return)

# Select the market capitalization
market_cap = components['Market Capitalization']

# Calculate the total market cap
total_market_cap = market_cap.sum()

# Calculate the component weights, and print the result
weights = market_cap.div(total_market_cap)
print(weights.sort_values())

# Calculate and plot the contribution by component
weights.mul(index_return).sort_values().plot(kind='barh')
plt.show()

# Convert index series to dataframe here
data = index.to_frame('Index')

# Normalize djia series and add as new column to data
djia = djia.div(djia.iloc[0]).mul(100)
data['DJIA'] = djia

# Show total return for both index and djia
print(data.iloc[-1].div(data.iloc[0], axis=0).sub(1).mul(100))

# Plot both series
data.plot()
plt.show()

# Inspect data
print(data.info())
print(data.head())

# Create multi_period_return function here
def multi_period_return(r):
    return (np.prod(r+1)-1) * 100

# Calculate rolling_return_360
rolling_return_360 = data.pct_change().rolling('360D').apply(multi_period_return)

# Plot rolling_return_360 here
rolling_return_360.plot(title='Rolling 360D Return')
plt.show()

# Inspect stock_prices here
print(stock_prices.info())

# Calculate the daily returns
returns = stock_prices.pct_change()

# Calculate and print the pairwise correlations
correlations = returns.corr()
print(correlations)

# Plot a heatmap of daily return correlations
sns.heatmap(correlations, annot= True)
plt.title('Daily Return Correlations')
plt.show()

# Inspect index and stock_prices
print(index.info())
print(stock_prices.info())

# Join index to stock_prices, and inspect the result
data = stock_prices.join(index)
print(data.info())

# Create index & stock price returns
returns = data.pct_change()

# Export data and data as returns to excel
with pd.ExcelWriter('data.xls') as writer:
    data.to_excel(excel_writer=writer, sheet_name="data")
    returns.to_excel(excel_writer=writer, sheet_name="returns")

