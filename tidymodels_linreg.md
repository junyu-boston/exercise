# modeling with tidymodels framework
1. Data resampling with **resample**
```
library(tidymodels)
mpg_split <- initial_split(mpg,
  prop = 0.75,
  strata = hwy)
mpg_training <- mpg_split %>%
training()
mpg_test <- mpg_split %>%
testing()
```

2. Fit model with parsnip package
```
lm_model <- linear_reg() %>%
set_engine('lm') %>%
set_mode('regression')
lm_fit <- lm_model %>%
fit(hwy ~ cty, data = mpg_training)

# obtaining the estimated parameters
tidy(lm_fit)

# Making predictions
hwy_predictions <- lm_fit %>%
predict(new_data = mpg_test)

# Names prediction column .pred

# Adding Predictions to the test data
mpg_test_results <- mpg_test %>%
select(hwy, cty) %>%
bind_cols(hwy_predictions)
```
3. Evaluate Model Performance With yardstick

All yardstick functions require a tibble with model results. The following codes to get RMSE and R squrared residues (coefficient of determination).

```
mpg_test_results %>%
rmse(truth = hwy, estimate = .pred)

mpg_test_results %>%
rsq(truth = hwy, estimate = .pred)

# R squared plot
ggplot(mpg_test_results, aes(x = hwy, y = .pred)) +
  geom_point() +
  geom_abline(color = 'blue', linetype = 2) +
  coord_obs_pred() +
  labs(title = 'R-Squared Plot',
    y = 'Predicted Highway MPG',
    x = 'Actual Highway MPG')
 
```

3. Streamlining model fitting: the last_fit() function

Takes a model speci,cation, model formula, and data split object

Performs the following:
- Creates training and test datasets
- Fits the model to the training data
- Calculates metrics and predictions on the test data
- Returns an object with all results

```
lm_last_fit <- lm_model %>%
  last_fit(hwy ~ cty,
  split = mpg_split)
  
lm_last_fit %>%
collect_metrics()

### collect test predictions
lm_last_fit %>%
collect_predictions()
```
