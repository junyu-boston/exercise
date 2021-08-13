# modeling with tidymodels framework
1. Data resampling with **resample**
```
library(tidymodels)
leads_split <- initial_split(leads_df, prop = 0.75, strata = purchased)
leads_training <- leads_split %>%
  training()
leads_test <- leads_split %>%
  testing()
```

2. Fit model with parsnip package
```
logistic_model <- logistic_reg() %>%
  set_engine('glm') %>%
  set_mode('classification')

logistic_fit <- logistic_model %>%
fit(purchased ~ total_visits + total_time,
data = leads_training)

# obtaining the estimated parameters
tidy(logistic_fit)

# Making predictions
class_preds <- logistic_fit %>%
predict(new_data = leads_test,
type = 'class')

prob_preds <- logistic_fit %>%
predict(new_data = leads_test,
type = 'prob')

# The predict() function will return a tibble with multiple columns. 
# One for each category of the outcome variable
# Naming convention is .pred_{outcome_category}

# Adding Predictions to the test data
leads_results <- leads_test %>%
select(purchased) %>%
bind_cols(class_preds, prob_preds)
```
3. Evaluate Model Performance With yardstick

All yardstick functions require a tibble with model results. The following codes to get RMSE and R squrared residues (coefficient of determination).

```
conf_mat(leads_results,
  truth = purchased,
  estimate = .pred_class)



accuracy(leads_results,
truth = purchased,
estimate = .pred_class)

sens(leads_results,
truth = purchased,
estimate = .pred_class)

spec(leads_results,
truth = purchased,
estimate = .pred_class)

custom_metrics <-
metric_set(accuracy, sens, spec)

custom_metrics(leads_results,
truth = purchased,
estimate = .pred_class)

## many indexes
conf_mat(leads_results, truth = purchased, estimate = .pred_class) %>%
summary()

```

4. Visualizing models

```
# confusion matrix
# Heatmap
conf_mat(leads_results,
truth = purchased,
estimate = .pred_class) %>%
autoplot(type = 'heatmap')

# Mosaic plot
conf_mat(leads_results, truth = purchased, estimate = .pred_class) %>% 
autoplot(type ='mosaic')

# ROC curve
leads_results %>%
roc_curve(truth = purchased, .pred_yes)

leads_results %>%
roc_curve(truth = purchased, .pred_yes) %>%
autoplot()

# calculate ROC AUC
roc_auc(leads_results,
truth = purchased,
.pred_yes)
```

5. Streamlining model fitting: the last_fit() function

Takes a model speci,cation, model formula, and data split object

Performs the following:
- Creates training and test datasets
- Fits the model to the training data
- Calculates metrics and predictions on the test data
- Returns an object with all results

```
leads_split <- initial_split(leads_df,
strata = purchased)
logistic_model <- logistic_reg() %>%
set_engine('glm') %>%
set_mode('classification')

logistic_last_fit <- logistic_model %>%
last_fit(purchased ~ total_visits + total_time,
split = leads_split)
logistic_last_fit %>%
collect_metrics()

last_fit_results <- logistic_last_fit %>%
collect_predictions()

custom_metrics(last_fit_results,
truth = purchased,
estimate = .pred_class,
.pred_yes)

```
