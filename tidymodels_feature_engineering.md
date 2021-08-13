# Feature engineering with the recipes package

like fit_transform in sklearn. recipe - step - prep - bake

1. continuous predictor variables

```
leads_log_rec <- recipe(purchased ~ ., data = leads_training) %>%
  step_log(total_time, base = 10)
leads_log_rec %>% summary()

leads_log_rec_prep <- leads_log_rec %>%
prep(training = leads_training)

leads_log_rec_prep %>%
bake(new_data = NULL)

leads_log_rec_prep %>%
bake(new_data = leads_test)

```

2. Numeric predictor variables
```
leads_log_rec_prep %>%
bake(new_data = leads_test)

# processing correlated predictors
leads_cor_rec <- recipe(purchased ~ .,
data = leads_training) %>%
step_corr(total_visits, total_time,
pages_per_visit, total_clicks,
threshold = 0.9)

leads_cor_rec <- recipe(purchased ~ .,
data = leads_training) %>%
step_corr(all_numeric(), threshold = 0.9)

leads_cor_rec %>%
prep(training = leads_training) %>%
bake(new_data = leads_test)

### Combining data preprocessing steps
leads_norm_rec <- recipe(purchased ~ .,
data = leads_training) %>%
step_corr(all_numeric(), threshold = 0.9) %>%
step_normalize(all_numeric())

leads_norm_rec %>%
prep(training = leads_training) %>%
bake(new_data = leads_test)
leads_cor_rec

```
2. Categorical data

```
# One hot encoding
# Maps categorical values to a sequence of [0/1] indicator variables
# Indicator variable for each unique value in original data
# or dummy variable encoding.

recipe(purchased ~ ., data = leads_training) %>%
step_dummy(lead_source, us_location) %>%
prep(training = leads_training) %>%
bake(new_data = leads_test)

recipe(purchased ~ ., data = leads_training) %>%
step_dummy(all_nominal(), -all_outcomes()) %>%
prep(training = leads_training) %>%
bake(new_data = leads_test)

```

3. A complete modeling example

```
# train-test splitting
leads_split <- initial_split(leads_df,
strata = purchased)
leads_training <- leads_split %>%
training()
leads_test <- leads_split %>%
testing()

# model defining
logistic_model <- logistic_reg() %>%
set_engine('glm') %>%
set_mode('classification')

# feature engineering
leads_recipe <- recipe(purchased ~ .,
data = leads_training) %>%
step_corr(all_numeric(), threshold = 0.9) %>%
step_normalize(all_numeric()) %>%
step_dummy(all_nominal(), -all_outcomes())

leads_recipe_prep <- leads_recipe %>%
prep(training = leads_training)

leads_training_prep <- leads_recipe_prep %>%
bake(new_data = NULL)
leads_training_prep

leads_test_prep <- leads_recipe_prep %>%
bake(new_data = leads_test)
leads_test_prep

# Model fitting and predictions
logistic_fit <- logistic_model %>%
fit(purchased ~ .,
data = leads_training_prep)

class_preds <- predict(logistic_fit,
new_data = leads_test_prep,
type = 'class')
prob_preds <- predict(logistic_fit,
new_data = leads_test_prep,
type = 'prob')

leads_results <- leads_test %>%
select(purchased) %>%
bind_cols(class_preds, prob_preds)
leads_results

# Model evaluation
leads_results %>%
conf_mat(truth = purchased,
estimate = .pred_class)



```
