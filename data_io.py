# This class is used for loading intermediate output file or raw file as an object
from sklearn.model_selection import train_test_split
import numpy as np

from utility import create_csr_matrix

class Data:
	def __init__(self, key_path):
		f = open(key_path, 'r')
		self.text = []
		self.marks = []
		self.status = False
		self.count = 0
		self.X_train = None
		self.X_test = None
		self.y_train = None
		self.y_test = None
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
		print("Shape("+str(len(self.text))+","+str(len(self.marks))+")")
		if(self.count>0):
			self.status = True
	
	def get_calculable_marks(self):
		float_marks = []
		print("get_calculable_marks="+str(len(self.marks)))
		for t in self.marks:
			float_marks.append([float(t)])
		
		return create_csr_matrix(float_marks)
	
	# Return the size of the data and size of column
	def shape(self):
		return (self.count, (2 if len(self.marks)>0 else 1) )
			
	def get_status(self):
		return self.status

	def shuffle_and_split(self, x_origin, y_origin):
		#skf = StratifiedKFold(n_splits = partition)
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x_origin, y_origin, train_size=0.75)

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

