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

class Classify:
	def __init__(self):
		self.classifiers = [(self.get_ridge_clf(), "Ridge Classifier"), (self.get_perceptron_clf(), "Perceptron"),
		(self.get_passive_aggr_clf(), "Passive-Aggressive"), (self.get_k_neighbors_clf(), "K Neighbors"),
		(self.get_rand_forest_clf(), "Random forest")]

	def get_ridge_clf(self):
		return RidgeClassifier(tol=1e-2, solver="lsqr")
	# max_iter and tol are necessary in the new implementation of logistic regression of scikit-learn. 
	# See https://github.com/scikit-learn/scikit-learn/issues/5022
	def get_perceptron_clf(self):
		return Perceptron(max_iter=50, tol=None)
	def get_passive_aggr_clf(self):
		return PassiveAggressiveClassifier(max_iter=50, tol=None)
	def get_k_neighbors_clf(self):
		return KNeighborsClassifier(n_neighbors=10)
	def get_rand_forest_clf(self):
		return RandomForestClassifier(n_estimators=100)

	# Code Ref from scikit-learn : 
	# http://scikit-learn.org/stable/auto_examples/text/document_classification_20newsgroups.html#sphx-glr-auto-examples-text-document-classification-20newsgroups-py
	def benchmark(self, clf, x_train, y_train, x_test, y_test):
		print('_' * 80)
		print("Training by: "+clf)
		
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
		print("Accuracy:   %0.3f" % score)
		
		print("Classification report:")
		print(metrics.classification_report(y_test, pred, target_names=str(clf)))
		
		print("Confusion matrix:")
		print(metrics.confusion_matrix(y_test, pred))
		
		#TODO: To understand this coefficient...
		if hasattr(clf, 'coef_'):
			print("Dimensionality: %d" % clf.coef_.shape[1])
			print("Density: %f" % density(clf.coef_))

		clf_descr = str(clf).split('(')[0]
		return clf_descr, score, train_time, test_time

#test = Classify()
#print(test.classifiers)
