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
	def __init__(self, clean_data_path):
		self.data = Data(clean_data_path)
		print("Data size: "+str(self.data.shape()))
		#min_df set to 2 to avoid unique id sequence
		self.count_model = CountVectorizer(min_df=2, max_features=5000, ngram_range=(1, 2), stop_words = "english")
	
	def get_X(self):
		word_counts = self.count_model.fit_transform(self.data.text)
		return TfidfTransformer().fit_transform(word_counts)
	
	def get_vocabulary_counts(self):
		word_counts = self.count_model.fit_transform(self.data.text)
		vocabs = self.count_model.get_feature_names()
		dic_to_tf = {}
		for i in range(word_counts.shape[1]):
			feature_count = word_counts.getcol(i).sum()
			if feature_count>1 :
				print("TF("+vocabs[i]+")="+str(feature_count))
				dic_to_tf[vocabs[i]] = feature_count
		return dic_to_tf
	
	def get_tf(self):
		word_counts = self.count_model.fit_transform(self.data.text)
		return TfidfTransformer(use_idf=False).fit_transform(word_counts)
	
test = TfIdf("dataset/trump/clean_data.txt")
test.get_vocabulary_counts()
print(test.get_X())
print(test.get_tf())
