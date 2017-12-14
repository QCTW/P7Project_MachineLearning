
import numpy as np
import re

from sklearn.feature_selection import f_classif
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from data_io import Data
from utility import get_unique_value_in_list

class TfIdf:
	def __init__(self, clean_data_path, num_of_class=2):
		self.features = None
		self.data = Data(clean_data_path)
		self.num_of_known_class = num_of_class
		self.max_num_of_features = 1000 #500*num_of_class
		#min_df set to 2 to avoid unique id sequence
		#max_df set to float depends on how many categories of data we have -- the more categories we have, the smaller max_df will be.
		self.count_model = CountVectorizer(min_df=2, max_df=float(1/num_of_class), max_features=self.max_num_of_features, stop_words = "english")
		#self.count_model = CountVectorizer(min_df=2, max_df=float(1/num_of_class), stop_words = "english")
		print("TfIdf created;load file shape;"+str(self.data.shape())+";max_features="+str(self.max_num_of_features)+";max_df="+str(float(1/num_of_class))+";stop_words='english'")
	
	def get_Y(self):
		return self.data.get_marks()
	
	def get_unique_Y(self):
		return get_unique_value_in_list(self.data.get_marks())

	# Return X and feature-names as tuple
	def get_X_by_vocabulary(self, input_txt=None):
		#TODO: To filter features by test_word.mean(x,y, 2) or ANOVA
		print("Counting "+str(self.max_num_of_features)+" normalized vocabularies...")
		used_model = self.count_model
		if input_txt != None:
			used_model = CountVectorizer(max_features=self.max_num_of_features, stop_words="english")
		else:
			input_txt = self.data.text

		word_counts = used_model.fit_transform(input_txt)
		
		#p_values = f_classif(word_counts, self.data.get_marks())
		#p_list = p_values[1].tolist()
		#for e in p_list:
			#print(e)
		#p_list.sort(key=lambda x: x[1])
		#print(p_list)
		return (TfidfTransformer().fit_transform(word_counts), used_model.get_feature_names())

	# Return X and feature-names as tuple
	def get_X_by_n_gram(self, n, input_txt=None):
		print("Counting "+str(self.max_num_of_features)+" normalized "+str(n)+"-grams...")
		used_model = None
		if input_txt == None:
			input_txt = self.data.text
			used_model = CountVectorizer(ngram_range=(n, n), min_df=2, max_df=float(1 / self.num_of_known_class), max_features=self.max_num_of_features, stop_words="english")
		else:
			used_model = CountVectorizer(ngram_range=(n, n), max_features=self.max_num_of_features, stop_words="english")
		
		counts = used_model.fit_transform(input_txt)
		return (TfidfTransformer().fit_transform(counts), used_model.get_feature_names())

	# Used for analysis content only
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

####################
# Unit test section
####################
#test = TfIdf("dataset/trump/clinton-trump-tweets_clean.csv", 2) #We known that there are 3 categories of data in the files
#test.get_vocabulary_counts()
#test.get_X_by_vocabulary()
#(bigrams, terms) = test.get_X_by_n_gram(2)
#for i in range(bigrams.shape[1]):
#	tf_sum = bigrams.getcol(i).sum()
#	print("TF("+terms[i]+")="+str(tf_sum))
	
#print(type(test.get_tf()))
#print("test.get_X_by_vocabulary()="+str(test.get_X_by_vocabulary().shape))
#test.data.shuffle_and_split(test.get_X_by_vocabulary(), test.data.get_calculable_marks())

#print(test.data.X_train)
#print(test.data.y_train)
