# The forward stepwise variable selection procedure

# Implementation of the AUC function:
from sklearn import linear_model
from sklearn.metrics import roc_auc_score

def auc(variables, target, basetable):
  X = basetable[variables]
  y = basetable[target]
  logreg = linear_model.LogisticRegression()
  logreg.fit(X, y)
  predictions = logreg.predict_proba(X)[:,1]
  auc = roc_auc_score(y, predictions)
  return(auc)

### example to use this funciton
auc = auc(["age","gender_F"],["target"],basetable)
print(round(auc,2))

# calculate the next best variable
def next_best(current_variables,candidate_variables, target, basetable):
  best_auc = -1
  best_variable = None
  for v in candidate_variables:
    auc_v = auc(current_variables + [v], target, basetable)
    if auc_v >= best_auc:
    best_auc = auc_v
    best_variable = v
  return best_variable

### Use function to get the next_best variable 
current_variables = ["age","gender_F"]
candidate_variables = ["min_gift","max_gift","mean_gift"]
next_variable = next_best(current_variables, candidate_variables, basetable)
print(next_variable)

# Write a loop to do forard stepwise variable selection.
candidate_variables = ["mean_gift", "min_gift", "max_gift", "age", "gender_F", "country_USA", "income_low"]
current_variables = []
target = ["target"]
max_number_variables = 5
number_iterations = min(max_number_variables, len(candidate_variables))
for i in range(0, number_iterations):
  next_var = next_best(current_variables,candidate_variables,target,basetable)
  current_variables = current_variables + [next_variable]
  candidate_variables.remove(next_variable)
print(current_variables)

# sklearn has class to do this:
import sklearn.feature_selection.SequentialFeatureSelector
