1. model specification

```
dt_model <- decision_tree() %>%
set_engine('rpart') %>%
set_mode('classification')
```

2. feature engineering

```
leads_recipe <- recipe(purchased ~ .,
data = leads_training) %>%
step_corr(all_numeric(), threshold = 0.9) %>%
step_normalize(all_numeric()) %>%
step_dummy(all_nominal(), -all_outcomes())
```

3. combining models and recipes

workflows package is to combine a parsnip model and recipe object into a single workflow object.This will specify model and transformation together.

```
leads_wkfl <- workflow() %>%
add_model(dt_model) %>%
add_recipe(leads_recipe)
```

4. Model fitting with workflows, and predict

```
leads_wkfl_fit <- leads_wkfl %>%
  last_fit(split = leads_split)
leads_wkfl_fit %>%
  collect_metrics()
  
leads_wkfl_preds <- leads_wkfl_fit %>%
collect_predictions()

# exploring custom metrics
leads_metrics <- metric_set(roc_auc, sens, spec)
leads_wkfl_preds %>%
leads_metrics(truth = purchased,
estimate = .pred_class,
.pred_yes)

```

5. Estimating performance with cross validation

```
# create cv folds
set.seed(214)
leads_folds <- vfold_cv(leads_training,
v = 10,
strata = purchased)

# model training with cv
# 1. use fit_resamples(), this will take care of cv, v_folds object replaces X_train, y_train
# 2. use workflow to fit, this packages model and recipe/bake together.
# 3. Optional custom metric function, metrics. This is the input to fit_resamples function.
leads_rs_fit <- leads_wkfl %>%
fit_resamples(resamples = leads_folds,
metrics = leads_metrics)
leads_rs_fit %>%
collect_metrics() # Average value in mean column

# Get detailed cv results for each Fold
rs_metrics <- leads_rs_fit %>%
collect_metrics(summarize = FALSE)

# Summarizing cross validation results, just dplyr
rs_metrics %>%
group_by(.metric) %>%
summarize(min = min(.estimate),
median = median(.estimate),
max = max(.estimate),
mean = mean(.estimate),
sd = sd(.estimate))
```

**The purpose of fit_resample() is to EVALUATE/SELECT MODELS**
- explore and compare the performance profile of different model types
- Select best performing model type and focus on model fitting efforts

6. Hyperparameter tunning - tune()

Labeling hyperparameters for tuning: set hyper-parameters to tune() in parsnip model specification. This lets other functions know that they need to be optimized.

```
dt_tune_model <- decision_tree(cost_complexity = tune(),
  tree_depth = tune(),
  min_n = tune()) %>%
  set_engine('rpart') %>%
  set_mode('classification')

```

Creating a tunning workflow

```
leads_wkfl <- workflow() %>%
  add_model(dt_model) %>%
  add_recipe(leads_recipe)

leads_tune_wkfl <- leads_wkfl %>%
  update_model(dt_tune_model)

```

Grid search, randam grid
```
set.seed(214)
dt_grid <- grid_random(parameters(dt_tune_model), size = 5)
```

Hyperperameter tuning with cv.

tune_grid can be thinked of a bigger fit_resamples, run many times with different parameters, performing hyperp tuning.

it takes workflow (preprocessing and model specification), resamples (cv), grid (hyperp tuning), and metrics (loss function) objects.

```
dt_tuning <- leads_tune_wkfl %>%
  tune_grid(resamples = leads_folds,
  grid = dt_grid,
  metrics = leads_metrics)


# exploring results get the average estimated metric values across all folds per combination
dt_tuning %>% collect_metrics()

# detailed results
dt_tuning %>%
collect_metrics(summarize = FALSE)

# summarize roc auc
dt_tuning %>%
collect_metrics(summarize = FALSE) %>%
filter(.metric == 'roc_auc') %>%
group_by(id) %>%
summarize(min_roc_auc = min(.estimate),
median_roc_auc = median(.estimate),
max_roc_auc = max(.estimate))

```

7. select the best model

```
# view the best model
dt_tuning %>% show_best(metric = 'roc_auc', n = 5)

# selecting a model
best_dt_model <- dt_tuning %>%
  select_best(metric = 'roc_auc')
  best_dt_model

# finalize the workflow
final_leads_wkfl <- leads_tune_wkfl %>%
  finalize_workflow(best_dt_model) # return a workflow object with set hyperp values

# model fitting
leads_final_fit <- final_leads_wkfl %>%
  last_fit(split = leads_split)
  leads_final_fit %>%
  collect_metrics()
```

**This is so exciting!**
