import numpy as np
import sys
from time import time

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split

class Classify:
	def __init__(self):
		self.classifiers = [	(self.get_nearest_centroid(), "Nearest Centroid (aka Rocchio)"),
		(self.get_multinomial_naive_bayes(), "Naive Bayes"),
		(self.get_ridge_clf(), "Ridge Classifier"), 
		(self.get_perceptron_clf(), "Perceptron"),
		(self.get_passive_aggr_clf(), "Passive-Aggressive"), 
		(self.get_k_neighbors_clf(), "K Neighbors"),
		(self.get_rand_forest_clf(), "Random Forest")]

	def get_multinomial_naive_bayes(self):
		return MultinomialNB(alpha=.01)
	def get_nearest_centroid(self):
		return NearestCentroid()
	def get_ridge_clf(self):
		return RidgeClassifier(tol=1e-2, solver="auto")
	# max_iter and tol are necessary in the new implementation of logistic regression of scikit-learn. 
	# See https://github.com/scikit-learn/scikit-learn/issues/5022
	def get_perceptron_clf(self):
		return Perceptron(max_iter=50, tol=None)
	def get_passive_aggr_clf(self):
		return PassiveAggressiveClassifier(max_iter=50, tol=None)
	def get_k_neighbors_clf(self, num_of_neigh=5):
		return KNeighborsClassifier(n_neighbors=num_of_neigh)
	def get_rand_forest_clf(self):
		return RandomForestClassifier(n_estimators=200)

# Code Ref from scikit-learn : 
# http://scikit-learn.org/stable/auto_examples/text/document_classification_20newsgroups.html#sphx-glr-auto-examples-text-document-classification-20newsgroups-py
def benchmark(clf, x_train, y_train, x_test, y_test, y_labels):
	print('=' * 80)
	print("Training by: "+str(clf))
	
	#TODO: To add StratifiedKFold to generate different split group and test each split group with train and predict
	t0 = time()
	clf.fit(x_train, y_train)
	train_time = time() - t0
	print("Training time: %0.3fs" % train_time)
	
	t0 = time()
	pred = clf.predict(x_test)
	test_time = time() - t0
	print("Predict time:  %0.3fs" % test_time)
	
	score = metrics.accuracy_score(y_test, pred)
	print("Accuracy:      %0.3f" % score)
	
	print("Classification report:")
	print(metrics.classification_report(y_test, pred, target_names=y_labels))
	
	print("Confusion matrix:")
	print(metrics.confusion_matrix(y_test, pred))
	
	#TODO: To understand this coefficient...
	if hasattr(clf, 'coef_'):
		print("Dimensionality: %d" % clf.coef_.shape[1])
		print("Density: %f" % density(clf.coef_))

	clf_descr = str(clf).split('(')[0]
	return clf_descr, score, train_time, test_time


# the code of the professor in # Ex4.5
def find_best_k_clf(x_train, y_train, x_test, y_test, algo_type, k_min, step_size, k_max, n_fold = 5):
    if k_min <= k_max and (algo_type == "knn" or algo_type == "rfc"):
        print("Divide the data set into %d parts for validation cross..." % n_fold)
        skf = StratifiedKFold(n_splits=n_fold)
        best_k = 1
        best_score = 0

        for k in range(k_min, k_max, step_size):
            score_sum = 0.0

            for train_idx, test_idx in skf.split(x_train, y_train):
                X_subtrain, X_subtest = x_train[train_idx], x_train[test_idx]
                y_subtrain, y_subtest = y_train[train_idx], y_train[test_idx]
                if algo_type == "rfc":
                    clf = RandomForestClassifier(n_estimators=k)
                else:
                    clf = KNeighborsClassifier(n_neighbors=k)
                clf.fit(X_subtrain, y_subtrain)
                score = clf.score(X_subtest, y_subtest)
                score_sum += score

            # get the average across splits
            score_sum /= n_fold
            print("For k", k, "Average_score is", score_sum)
            if score_sum > best_score:
                best_score = score_sum
                best_k = k

        # re-launch on the whole dataset
        if algo_type == "rfc":
            clf_total = RandomForestClassifier(n_estimators=best_k)
        else:
            clf_total = KNeighborsClassifier(n_neighbors=best_k)
        clf_total.fit(x_train, y_train)
        score = clf_total.score(x_test, y_test)

        # for example "Best K is 1, with a score of 0.939..."
        print("Best K is", best_k, "with a score of", score)

    else:
        print("Error, k_min greater than k_max")


####################
# Unit test section
####################
#test = Classify()
#print(test.classifiers)
