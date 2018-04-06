# This class is used for loading intermediate output file or raw file as an object
from sklearn.model_selection import train_test_split
from utility import create_csr_matrix
import numpy as np
import pandas as pd

class Data:
	def __init__(self, key_path):
		self.text = []
		self.marks = []
		self.status = False
		self.count = 0
		self.X_train = None
		self.X_test = None
		self.y_train = None
		self.y_test = None
		if(len(key_path)>0):
			f = open(key_path, 'r')
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
		if(len(self.text)!=len(self.marks)):
			raise ValueError("Text X has different size ("+str(len(self.text))+") than Marks Y ("+str(len(self.marks))+")! Break-line must be removed from each line of text.")
		else:
			if(self.count>0):
				self.status = True
	
	def set_text_and_mark_from_dataframe(self, dataframe, x_col_name, y_col_name):
		self.text = dataframe[x_col_name].values.astype('U').tolist()
		self.marks = dataframe[y_col_name].values.astype('U').tolist()
	
	def set_text_and_mark(self, txt_list, mark_list):
		if(len(txt_list)==len(mark_list)):
			self.text = txt_list
			self.marks = mark_list
		else:
			raise ValueError("Unable to set_text_and_mark(): Text list and mark list are not the same size!")

	def get_marks(self):
		return np.array(self.marks)
	
	# Return the size of the data and size of column
	def shape(self):
		return (self.count, (2 if len(self.marks)>0 else 1) )
	
	# Usually this represent how many categories we want to classify
	def get_num_of_unique_Y(self):
		return len(list(set(self.marks)))
			
	def get_status(self):
		return self.status

	def shuffle_and_split(self, x_origin, y_origin):
		#skf = StratifiedKFold(n_splits = partition)
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x_origin, y_origin, train_size=0.75)

	def get_train_data(self):
		return (self.X_train, self.y_train)

	def get_test_data(self):
		return (self.X_test, self.y_test)
	
	def add_new_data(self, path_to_new_file):
		f = open(path_to_new_file, 'r')
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


####################
# Unit test section
####################
#test_data = Data("dataset/trump/clinton-trump-tweets_clean.csv")
#print(test_data.count)
#print(test_data.text[0])
#print(test_data.marks[0])

# X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
# y = np.array([1, 1, 2, 2, 3, 3])

