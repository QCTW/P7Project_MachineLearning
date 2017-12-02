import sklearn
import numpy as np
import re

from scipy.stats import ttest_ind
from sklearn.feature_extraction.text import TfidfVectorizer

from data_io import *

print("Use sklearn version: "+sklearn.__version__)

class TfIdf:
	def __init__(self, clean_data_path):
		self.data = Data(clean_data_path)
		print(self.data.text)
		self.model = TfidfVectorizer(min_df=0.001, stop_words = "english")
		self.X = self.model.fit_transform(self.data)
		self.features = self.model.get_feature_names()
		
	def get_matrix_x(self):
		return self.X
	
	def get_features(self):
		return self.features
	
test = TfIdf("dataset/trump/realDonaldTrump.csv")
print(test.get_features())
