#!/usr/bin/python

import sys
sys.path.append("../tools/")
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, GridSearchCV
from sklearn.naive_bayes import GaussianNB
from time import time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pprint import pprint
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

## Below are the functions created that are used later on in the code

def add_features_ratio(my_dataset,new_feature, feature_nominator, feature_denominator):
    for person in my_dataset:
        if (my_dataset[person][feature_nominator] !='NaN') & (my_dataset[person][feature_denominator] !='NaN'):
            my_dataset[person][new_feature] = float(my_dataset[person][feature_nominator]) / float(my_dataset[person][feature_denominator])
        else:
            my_dataset[person][new_feature] = 'NaN'
    return my_dataset

def optimal_feature_estimator(pipeline, param_grid, sss, features, labels):
    grid = GridSearchCV(pipeline, param_grid, verbose = 0, cv = sss, scoring = 'f1')
    t0 = time()
    grid.fit(features, labels)
    print "training time: ", round(time()-t0, 3), "s"
    print grid.best_params_
    return grid.best_estimator_, grid.best_score_ 


def optimal_features_scores_calculation(n_splits, sss, clf, features, labels):
    df = pd.DataFrame(0, index=np.arange(1,n_splits), columns=['accuracy_score','precision','recall','f1_score'])
    df.index.name = 'n_split'
#    sss = StratifiedShuffleSplit(n_splits, test_size, random_state)
    for i, (e_train, e_test) in enumerate(sss.split(features, labels)):
        features_test = []
        labels_test = []
        features_train = []
        labels_train = []
        for k in e_train:
            labels_train.append(labels[k])
            features_train.append(features[k])
        for k in e_test:
            labels_test.append(labels[k])
            features_test.append(features[k])
        clf.fit(features_train,labels_train)
        prediction = clf.predict(features_test)
        df.loc[i,'accuracy_score'] = accuracy_score(labels_test, prediction)
        df.loc[i,'precision'] = precision_score(labels_test, prediction)
        df.loc[i,'recall'] = recall_score(labels_test, prediction)
        df.loc[i,'f1_score'] = f1_score(labels_test, prediction)
    return df.mean(axis=0)

def f1score_calculation_varying_feature(n_splits, sss, clf, numb_features, features, labels):
    df = pd.DataFrame(0, index=np.arange(1,n_splits), columns=['f1_score'])
    df.index.name = 'n_split'
    features_reduced = SelectKBest(f_classif, k=numb_features).fit_transform(features, labels)
#    sss = StratifiedShuffleSplit(n_splits, test_size, random_state)
    for i, (e_train, e_test) in enumerate(sss.split(features_reduced, labels)):
        features_test = []
        labels_test = []
        features_train = []
        labels_train = []
        for k in e_train:
            labels_train.append(labels[k])
            features_train.append(features_reduced[k])
        for k in e_test:
            labels_test.append(labels[k])
            features_test.append(features_reduced[k])
        clf.fit(features_train,labels_train)
        prediction = clf.predict(features_test)
        df.loc[i,'accuracy_score'] = accuracy_score(labels_test, prediction)
        df.loc[i,'precision'] = precision_score(labels_test, prediction)
        df.loc[i,'recall'] = recall_score(labels_test, prediction)
        df.loc[i,'f1_score'] = f1_score(labels_test, prediction)
    return df.mean(axis=0)


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi',
 'expenses',
 'deferred_income',
 'long_term_incentive',
 'other',
 'fraction_shared_receipt_with_poi',
 'bonus',
 'total_stock_value',
 'from_poi_to_this_person',
 'restricted_stock',
 'fraction_from_this_person_to_poi',
 'salary',
 'total_payments',
 'exercised_stock_options'] # You will need to use more features
#, 'total payments'
### Load the dictionary containing the dataset

###Below the features created including all and non new to compare the efficiency of algorithms for different scenarios
features_list_non_new_features = ['poi',
 'expenses',
 'deferred_income',
 'long_term_incentive',
 'other',
 'bonus',
 'total_stock_value',
 'from_poi_to_this_person',
 'restricted_stock',
 'salary',
 'total_payments',
 'exercised_stock_options']

features_list_all = ['poi',
 'salary',
 'to_messages',
 'deferral_payments',
 'total_payments',
 'fraction_shared_receipt_with_poi',
 'exercised_stock_options',
 'bonus',
 'restricted_stock',
 'shared_receipt_with_poi',
 'fraction_from_this_person_to_poi',
 'restricted_stock_deferred',
 'total_stock_value',
 'expenses',
 'loan_advances',
 'from_messages',
 'other',
 'from_this_person_to_poi',
 'director_fees',
 'deferred_income',
 'long_term_incentive',
 'from_poi_to_this_person']


def open_dataset():
    with open("final_project_dataset.pkl", "r") as data_file:
        data_dict = pickle.load(data_file)
    return data_dict
my_dataset = open_dataset()


### Task 2: Remove outliers
## Remove outliers identified 'TOTAL' and 'THE TRAVEL AGENCY IN THE PARK')

my_dataset.pop('THE TRAVEL AGENCY IN THE PARK',0)
my_dataset.pop('TOTAL',0)
if ('TOTAL' or 'THE TRAVEL AGENCY IN THE PARK') in my_dataset:
    print 'outliers still there'
else:
    print 'outliers removed'

    
### The two outliers found in the dataset were the ones with the keys in the 

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

my_dataset = add_features_ratio(my_dataset=my_dataset, new_feature='fraction_from_this_person_to_poi', feature_nominator='from_this_person_to_poi', feature_denominator='from_messages')
my_dataset = add_features_ratio(my_dataset=my_dataset, new_feature='fraction_shared_receipt_with_poi', feature_nominator='shared_receipt_with_poi', feature_denominator='to_messages')



### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list_all, sort_keys = True)
labels, features = targetFeatureSplit(data)
#print features
selector = SelectKBest(score_func=f_classif, k=5)
clf = selector.fit_transform(features, labels)
pprint(sorted(zip(selector.scores_, features_list_all[1:]), reverse=True))
#print (clf)


### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.


sss = StratifiedShuffleSplit(n_splits=100, test_size=0.3, random_state=32)
skb = SelectKBest(f_classif)

###Code to show the f1score vs the number of features in a chart including all features
f1_score_Gaussian = []
f1_score_KNN = []
f1_score_DT = []
feature_array = range(1,len(features_list_all))
clf_gaussian_NB = GaussianNB()
clf_knn = KNeighborsClassifier()
clf_dtree = DecisionTreeClassifier()
for numb_feature in feature_array: 
#for feature in [3,10]: 
    scores_Gaussian = f1score_calculation_varying_feature(n_splits=100, sss=sss, clf=clf_gaussian_NB, numb_features=numb_feature, features=features, labels=labels)
    f1_score_Gaussian.append(scores_Gaussian['f1_score'])
    scores_KNN = f1score_calculation_varying_feature(n_splits=100, sss=sss, clf=clf_knn, numb_features=numb_feature, features=features, labels=labels)
    f1_score_KNN.append(scores_KNN['f1_score'])
    scores_DT = f1score_calculation_varying_feature(n_splits=100, sss=sss, clf=clf_dtree, numb_features=numb_feature, features=features, labels=labels)
    f1_score_DT.append(scores_DT['f1_score'])
    
plt.plot(feature_array,f1_score_Gaussian, label='Gaussian_NB')
plt.plot(feature_array,f1_score_KNN, label='KNN Algorithm')
plt.plot(feature_array,f1_score_DT, label='Decision Tree')
plt.title('Algorithm performance for different number of features')
plt.xlabel('number of features')
plt.ylabel('f1 score')
plt.legend()
plt.show()

##Algorithm 1 GaussianNaive Bayes
clf_gaussian_NB = GaussianNB()
pipeline_GaussianNB = Pipeline(steps = [("SKB", skb), ("NaiveBayes",clf_gaussian_NB)])
param_grid_GaussianNB = {"SKB__k": range(1,len(features_list))}
clf_Gaussian_best, f1score_GaussianNB = optimal_feature_estimator(pipeline=pipeline_GaussianNB, param_grid=param_grid_GaussianNB, sss=sss, features=features, labels=labels)
scores_Gaussian_NB = optimal_features_scores_calculation(n_splits=100, sss=sss, clf=clf_Gaussian_best, features=features, labels=labels)
print 'scores Gaussian NB', scores_Gaussian_NB
  
  
##Algorithm 2 K Nearest Neighbours
  
clf_knn = KNeighborsClassifier()
scaler = MinMaxScaler()
skb = SelectKBest(f_classif)
pipeline_knn = Pipeline(steps = [("scaling", scaler), ("SKB", skb), ("knn",clf_knn)])
param_grid_knn = {"SKB__k": range(1,len(features_list)), "knn__n_neighbors": range(1,len(features_list))}
clf_knn_best, f1score_knn = optimal_feature_estimator(pipeline=pipeline_knn, param_grid=param_grid_knn, sss=sss, features=features, labels=labels)
scores_knn = optimal_features_scores_calculation(n_splits=100, sss=sss, clf=clf_knn_best, features=features, labels=labels)
print 'scores K neareast Neighbour', scores_knn
  
###Algorithm 3 Decision Tree Classifier
clf_dtree = DecisionTreeClassifier()
pipeline_DT = Pipeline(steps = [("SKB", skb), ("DT",clf_dtree)])
param_grid_DT = {"SKB__k": range(1,len(features_list)), 'DT__max_depth': [2,5,10,15,20], 'DT__min_samples_split': [2,4,6,8,10], 'DT__criterion': ['gini','entropy']}
clf_DT_best, f1score_DT = optimal_feature_estimator(pipeline=pipeline_DT, param_grid=param_grid_DT, sss=sss, features=features, labels=labels)
scores_DT = optimal_features_scores_calculation(n_splits=100, sss=sss, clf=clf_DT_best, features=features, labels=labels)
print 'scores Decision Tree', scores_DT



# ##Algorithm 1 GaussianNaive Bayes
# clf_gaussian_NB = GaussianNB()
# pipeline_GaussianNB = Pipeline(steps = [("SKB", skb), ("NaiveBayes",clf_gaussian_NB)])
# param_grid_GaussianNB = {"SKB__k": range(1,len(features_list_non_new_features))}
# clf_Gaussian_best, f1score_GaussianNB = optimal_feature_estimator(pipeline=pipeline_GaussianNB, param_grid=param_grid_GaussianNB, sss=sss, features=features, labels=labels)
# scores_Gaussian_NB = optimal_features_scores_calculation(n_splits=100, sss=sss, clf=clf_Gaussian_best, features=features, labels=labels)
# print 'scores Gaussian NB', scores_Gaussian_NB
# 
# 
# ##Algorithm 2 K Nearest Neighbours
# 
# clf_knn = KNeighborsClassifier()
# scaler = MinMaxScaler()
# skb = SelectKBest(f_classif)
# pipeline_knn = Pipeline(steps = [("scaling", scaler), ("SKB", skb), ("knn",clf_knn)])
# param_grid_knn = {"SKB__k": range(1,len(features_list_non_new_features)), "knn__n_neighbors": range(1,len(features_list_non_new_features))}
# clf_knn_best, f1score_knn = optimal_feature_estimator(pipeline=pipeline_knn, param_grid=param_grid_knn, sss=sss, features=features, labels=labels)
# scores_knn = optimal_features_scores_calculation(n_splits=100, sss=sss, clf=clf_knn_best, features=features, labels=labels)
# print 'scores K neareast Neighbour', scores_knn
# 
# ###Algorithm 3 Decision Tree Classifier
# clf_dtree = DecisionTreeClassifier()
# pipeline_DT = Pipeline(steps = [("SKB", skb), ("DT",clf_dtree)])
# param_grid_DT = {"SKB__k": range(1,len(features_list_non_new_features)), 'DT__max_depth': [2,5,10,15,20], 'DT__min_samples_split': [2,4,6,8,10], 'DT__criterion': ['gini','entropy']}
# clf_DT_best, f1score_DT = optimal_feature_estimator(pipeline=pipeline_DT, param_grid=param_grid_DT, sss=sss, features=features, labels=labels)
# scores_DT = optimal_features_scores_calculation(n_splits=100, sss=sss, clf=clf_DT_best, features=features, labels=labels)
# print 'scores Decision Tree', scores_DT


if (f1score_GaussianNB > f1score_knn) & (f1score_GaussianNB > f1score_DT):
    clf = clf_Gaussian_best
    print 'best algorithm is Gaussian NB with f1 score', f1score_GaussianNB
elif (f1score_knn > f1score_GaussianNB) & (f1score_knn > f1score_DT):
    clf = clf_knn_best
    print 'best algorithm is K Nearest Neighbour with f1 score', f1score_knn
else:
    clf = clf_DT_best
    print 'best algorithm is Decision Tree with f1 score', f1score_DT

    
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
# from sklearn.model_selection import train_test_split
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)