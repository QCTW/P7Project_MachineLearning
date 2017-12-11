import sklearn
import numpy as np
import re

from scipy.stats import ttest_ind
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from data_io import *

print("Use sklearn version: "+sklearn.__version__)

class TfIdf:
	def __init__(self, clean_data_path, num_of_class=2):
		self.data = Data(clean_data_path)
		self.num_of_known_class = num_of_class
		print("Data size: "+str(self.data.shape()))
		#min_df set to 2 to avoid unique id sequence
		#max_df set to float depends on how many categories of data we have -- the more categories we have, the smaller max_df will be.
		self.count_model = CountVectorizer(min_df=2, max_df=float(1/num_of_class), max_features=1000, stop_words = "english")
	
	def get_X_by_vocabulary(self):
		word_counts = self.count_model.fit_transform(self.data.text)
		return TfidfTransformer().fit_transform(word_counts)

	def get_X_by_n_gram(self, n):
		model = CountVectorizer(ngram_range=(n, n), min_df=2, max_df=float(1/self.num_of_known_class), max_features=1000, stop_words = "english")
		counts = model.fit_transform(self.data.text)
		terms = model.get_feature_names()
		return (TfidfTransformer().fit_transform(counts), terms)

	def get_vocabulary_counts(self):
		word_counts = self.count_model.fit_transform(self.data.text)
		vocabs = self.count_model.get_feature_names()
		dic_to_tf = {}
		for i in range(word_counts.shape[1]):
			feature_sum = word_counts.getcol(i).sum()
			print("TF("+vocabs[i]+")="+str(feature_sum))
			dic_to_tf[vocabs[i]] = feature_sum
		return dic_to_tf
	
	def get_tf(self):
		word_counts = self.count_model.fit_transform(self.data.text)
		return TfidfTransformer(use_idf=False).fit_transform(word_counts)
	
test = TfIdf("dataset/trump/clinton-trump-tweets_clean.csv", 2) #We known that there are 3 categories of data in the files
test.get_vocabulary_counts()
print(test.get_X_by_vocabulary())
(bigrams, terms) = test.get_X_by_n_gram(2)
for i in range(bigrams.shape[1]):
	tf_sum = bigrams.getcol(i).sum()
	print("TF("+terms[i]+")="+str(tf_sum))
print(type(test.get_tf()))

test.data.cv_partition(test.get_X_by_vocabulary, test.data.marks, 3)
print(test.data.n_partition)
