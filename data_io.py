# This class is used for loading intermediate output file or raw file as an object
from sklearn.model_selection import StratifiedKFold
import numpy as np

class Data:
	def __init__(self, key_path):
		f = open(key_path, 'r')
		self.text = []
		self.marks = []
		self.status = False
		self.count = 0
		self.n_partition = 0
		self.train_folds = []
		self.test_folds = []
		for line in f:
			one_line = line.strip()
			if(len(one_line)!=0):
				self.count+=1
				index_of_tab = one_line.find('\t')
				if(index_of_tab>0):
					first_col = one_line[:index_of_tab]
					second_col = one_line[index_of_tab+1:].strip()
					self.text.append(second_col)
					self.marks.append(first_col)
					#print("["+first_col+"] "+second_col)
				else:
					self.text.append(one_line)
		f.close()
		if(self.count>0):
			self.status = True
	
	# Return the size of the data and size of column
	def shape(self):
		return (self.count, (2 if len(self.marks)>0 else 1) )
			
	def get_status(self):
		return self.status

	def split(self, x, y, partition=5):
		self.n_partition = partition
		skf = StratifiedKFold(n_splits = partition)
		for train_idx, test_idx in skf.split(x, y):
			print("Train Index:", train_idx, ",Test Index:", test_idx)
			self.train_folds.append(train_idx)
			self.test_folds.append(test_idx)

	def get_train_data(self):
		return self.train_folds

	def get_test_data(self):
		return self.test_folds

	def get_partition(self):
		return self.n_partition

test_data = Data("dataset/trump/clinton-trump-tweets_clean.csv")
print(test_data.count)
print(test_data.text[0])
print(test_data.marks[0])

# X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
# y = np.array([1, 1, 2, 2, 3, 3])

