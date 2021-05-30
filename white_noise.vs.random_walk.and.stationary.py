import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### simulate a Gaussian White Noise Time Series
### for a white noise time series, all the autocorrelations are close to zero, so the past will not forecast the future.
# Import the plot_acf module from statsmodels
from statsmodels.graphics.tsaplots import plot_acf

# Simulate white noise returns:
# np.random.normal() creates an array of normally distributed random numbers.
# The loc argument is the mean and the scale argument is the standard deviation.
# This is one way to generate a white noise series.
returns = np.random.normal(loc=0.02, scale=0.05, size=1000)

# Print out the mean and standard deviation of returns
mean = np.mean(returns)
std = np.std(returns)
print("The mean is %5.3f and the standard deviation is %5.3f" %(mean,std))

# Plot returns series
plt.plot(returns)
plt.show()

# Plot autocorrelation function of white noise returns
plot_acf(returns, lags=20)
plt.show()

### Random Walk: 
### The current observation is a random step from the previous observation.
### In a random walk, today’s price is equal to yesterday’s price plus some noise. 
### The change in price of a random walk is just White Noise.
###  if stock prices follow a random walk, then stock returns are White Noise.

### Simulate stock price as random walk:
import matplotlib.pyplot as plt
# Generate 500 random steps with mean=0 and standard deviation=1
steps = np.random.normal(loc=0, scale=1, size=500)

# Set first element to 0 so that the first price will be the starting stock price
steps[0]=0

# Simulate stock prices, P with a starting price of 100
P = 100 + np.cumsum(steps)

# Plot the simulated stock prices
plt.plot(P)
plt.title("Simulated Random Walk")
plt.show()

### Random Walk with Drift
# Generate 500 random steps
# Generate 500 random normal multiplicative "steps" with mean 0.1% and
# standard deviation 1% using np.random.normal(), which are now returns,
# and add one for total return.
steps = np.random.normal(loc=0.001, scale=0.01, size=500) + 1

# Set first element to 1
steps[0]=1

# Simulate the stock price, P, by taking the cumulative product
P = 100 * np.cumprod(steps) 

# Plot the simulated stock prices
plt.plot(P)
plt.title("Simulated Random Walk with Drift")
plt.show()

### Run the Augmented Dickey-Fuller test to check if the time series is a Random Walk
AMZN = pd.read_csv('data/AMZN.csv', index_col='Date', parse_dates=True)
# Import the adfuller module from statsmodels
from statsmodels.tsa.stattools import adfuller

# Run the ADF test on the price series and print out the results
results = adfuller(AMZN['Adj Close'])
print(results)

# Just print out the p-value
print('The p-value of the test on prices is: ' + str(results[1]))

# Create a DataFrame of AMZN returns
AMZN_ret = AMZN.pct_change()

# Eliminate the NaN in the first row of returns
AMZN_ret = AMZN_ret.dropna()

# Run the ADF test on the return series and print out the p-value
results = adfuller(AMZN_ret['Adj Close'])
print('The p-value of the test on returns is: ' + str(results[1]))

### Stationarity:  the joint distribution of the observations do not depend on time.
### Weak Stationarity: the mean, variance, and autocorrelations of the observations do not depend on time.
### Transformation 
### Seasonal Adjustment

# Import the acf module and the plot_acf module from statsmodels
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf
import warnings
warnings.filterwarnings('ignore')

HRB = pd.read_csv('data/HRB.csv', index_col=['Quarter'], parse_dates=True)

# Compute the acf array of HRB
acf_array = acf(HRB)

# Plot the acf function, pass alpha=1 to suppress the confidence interval
plot_acf(HRB, lags=20, alpha=0.05)
plt.show()

# Seasonally adjust quarterly earnings
HRBsa = HRB.diff(4)

# Print the first 10 rows of the seasonally adjusted series
print(HRBsa.head(10))

# Drop the NaN data in the first four rows
HRBsa = HRBsa.dropna()

# Plot the autocorrelation function of the seasonally adjusted series
plot_acf(HRBsa)
plt.show()


