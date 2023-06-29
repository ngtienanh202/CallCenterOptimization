import xgboost as xgb
from sklearn import metrics
from xgboost import XGBClassifier




def modelfit(alg, dtrain, target, predictors,useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    """
    It takes in a model, a training set, a target variable, and a list of predictors, and then performs
    cross-validation to find the optimal number of boosting rounds.
    
    :param alg: the model
    :param dtrain: the training dataframe
    :param target: The target variable we are trying to predict
    :param predictors: The list of predictors that we want to use to train the model
    :param useTrainCV: If True, then use cross validation to find the optimal number of boosting rounds,
    defaults to True (optional)
    :param cv_folds: Number of cross-validation folds, defaults to 5 (optional)
    :param early_stopping_rounds: Activates early stopping. Validation error needs to decrease at least
    every <early_stopping_rounds> round(s) to continue training, defaults to 50 (optional)
    """
    
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(data= dtrain[predictors].values, label=dtrain[target].values)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds,
            metrics='auc', early_stopping_rounds=early_stopping_rounds)
        alg.set_params(n_estimators=cvresult.shape[0])
    
    #Fit the algorithm on the data
    alg.fit(dtrain[predictors].values, dtrain['Result'].values,eval_metric='auc')
        
    #Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]
        
    #Print model report:
    print("\nModel Report")
    print ("Accuracy : %.4g" % metrics.accuracy_score(dtrain['Result'].values, dtrain_predictions))
    print ("AUC Score (Train): %f" % metrics.roc_auc_score(dtrain['Result'], dtrain_predprob))

def FineTuningCV(data, target):
    """
    It takes in a dataframe and a target variable, and returns a model with the best parameters
    
    :param data: the dataframe containing the data
    :param target: The target variable we're trying to predict
    """
    predictors = [a for a in data.columns if a not in [target]]
    xgb1 = XGBClassifier(tree_method='gpu_hist', gpu_id=0,
    learning_rate =0.1,
    n_estimators=1000,
    max_depth=5,
    min_child_weight=1,
    gamma=0,
    subsample=0.8,
    colsample_bytree=0.8,
    objective= 'binary:logistic',
    nthread=4,
    scale_pos_weight=1,
    seed=27)
    modelfit(xgb1, data, predictors)

def GridSearchCV(data, predictors, target):
    """
    The function takes in the data, the predictors, and the target. It then creates a grid search object
    that will test the max_depth and min_child_weight parameters. The grid search object will use the
    XGBClassifier model, and will use 5-fold cross validation. The function will then fit the grid
    search object to the data, and return the results, the best parameters, and the best score
    
    :param data: the dataframe containing the data
    :param predictors: the features we want to use to predict the target
    :param target: the target variable
    """
    param_test1 = {
    'max_depth':range(3,10,2),
    'min_child_weight':range(1,6,2)
    }
    gsearch1 = GridSearchCV(estimator = XGBClassifier(tree_method='gpu_hist', gpu_id=0, learning_rate =0.1, n_estimators=140, max_depth=5,
    min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
    objective= 'binary:logistic', nthread=4, scale_pos_weight=1, seed=27), 
    param_grid = param_test1, scoring='roc_auc',n_jobs=4, cv=5)
    gsearch1.fit(data[predictors],data[target])
    gsearch1.cv_results_, gsearch1.best_params_, gsearch1.best_score_

def saveModel(model, path):
    """
    > The function takes in a model and a path, and saves the model to the path
    
    :param model: the model to save
    :param path: The path to save the model to
    """
    model.save_model(path)

