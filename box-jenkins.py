### 1. Identification
# Plot time series
savings.plot()
plt.show()

# Run Dicky-Fuller test
result = adfuller(savings)

# Print test statistic
print(result)

# Print p-value
print(result[1])

# Create figure
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
 
# Plot the ACF of savings on ax1
plot_acf(savings, zero=False,lags=10, ax=ax1)

# Plot the PACF of savings on ax2
plot_pacf(savings, zero=False, lags=10, ax=ax2)

plt.show()

### 2. Estimation
# Loop over p values from 0-3
order_aid_bic = []
for p in range(4):
  
  # Loop over q values from 0-3
    for q in range(4):
      try:
        # Create and fit ARMA(p,q) model
        model = SARIMAX(savings, order=(p, 0, q), trend='c')
        results = model.fit()
        
        # Print p, q, AIC, BIC
        print(p, q, results.aic, results.bic)
        order_aic_bic.append((p, q, results.aic, results.bic))
        
      except:
        print(p, q, None, None)
        order_aic_bic.append((p, q, None, None))
        
order_df = pd.DataFrame(order_aic_bic, columns=['p', 'q', 'aic', 'bic']
                         
### 3. Diagnosis
# Create and fit model
model = SARIMAX(savings, order=(1, 0, 2), trend='c')
results = model.fit()

# Create the 4 diagostics plots
results.plot_diagnostics()
plt.show()

# Print summary
print(results.summary())

