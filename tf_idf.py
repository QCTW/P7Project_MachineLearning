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
		print("Data size: "+str(self.data.shape()))
		#min_df set to 2 to avoid unique id sequence
		self.model = TfidfVectorizer(min_df=2, stop_words = "english")

	def get_matrix_x(self):
		return self.model.fit_transform(self.data.text)
	
	def get_vocabularies(self):
		self.model.fit_transform(self.data.text)
		return self.model.get_feature_names()
	
test = TfIdf("dataset/trump/clean_data.txt")
print(test.get_vocabularies())
print(test.get_matrix_x())