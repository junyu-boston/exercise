### normal distribution: simulation vs computation
set.seed(123)

# Generate data points
data_points <- rnorm(n = 1000)

# Inspect the distribution
hist(data_points)

# Compute the sample probability and print it
sample_probability <- mean(data_points <= 2)
print(sample_probability)

# Compute the true probability and print it
true_probability <- pnorm(q = 2)
print(true_probability) 

### Simulation for The law of large numbers: 
### the average of the results obtained from trials will tend to become closer to the expected value as more trials are performed.
set.seed(1)

# Create a sample of 20 die rolls
small_sample <- sample(1:6, size = 20, replace = TRUE)

# Calculate the mean of the small sample
mean(small_sample)

# Create a sample of 1000 die rolls
big_sample <- sample(1:6, size=1000, replace=TRUE)

# Calculate the mean of the big sample
mean(big_sample)

### Simulating central limit theorem
# Simulate 1000 die roll outputs
for (i in 1:1000) {
    die_outputs[i] <- sample(1:6, size = 1)
}

# Visualize the number of occurrences of each result
barplot(table(die_outputs))

# Calculate 1000 means of 30 die roll outputs
for (i in 1:1000) {
    mean_die_outputs[i] <- mean(sample(1:6, size = 30, replace = TRUE))
}

# Inspect the distribution of the results
hist(mean_die_outputs)

# The distribution of the results of rolling the dice is uniform, 
# but the distribution of samples' means is bell-shaped! 
# You can apply the probabilistic and statistical methods 
# that work for normal distributions to the distribution of samples' means.
