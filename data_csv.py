# This class is used for loading intermediate output file or raw file as an object
from sklearn.model_selection import train_test_split
from utility import create_csr_matrix
import numpy as np
import csv

class CsvData:
	def __init__(self, csv_path):
		self.text = []
		self.marks = []
		self.ids = []
		self.status = False
		self.count = 0
		self.X_train = None
		self.X_test = None
		self.y_train = None
		self.y_test = None
		with open(csv_path, newline='') as csv_file:
			reader = csv.DictReader(csv_file)
			for line in reader:
				self.count += 1
				self.text.append(line['comment_text'])
				self.ids.append(line['id'])
				print(str(type(line))+":"+line)
				if "author" in line:
					self.marks.append(line['author'])

		if(len(self.text)!=len(self.ids)):
			raise ValueError("Text X has different size ("+len(self.text)+") than Marks Y ("+len(self.marks)+")! Break-line must be removed from each line of text.")
		else:
			if(self.count>0):
				self.status = True
	
	def get_marks(self):
		return np.array(self.marks)
	
	# Return the size of the data and size of column
	def shape(self):
		return (self.count, (3 if len(self.marks)>0 else 1) )
	
	# Usually this represent how many categories we want to classify
	def get_num_of_unique_Y(self):
		return len(list(set(self.marks)))
			
	def get_status(self):
		return self.status

	def shuffle_and_split(self, x_origin, y_origin):
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x_origin, y_origin, train_size=0.75)

	def get_train_data(self):
		return (self.X_train, self.y_train)

	def get_test_data(self):
		return (self.X_test, self.y_test)


####################
# Unit test section
####################
#test_data = Data("dataset/trump/clinton-trump-tweets_clean.csv")
#print(test_data.count)
#print(test_data.text[0])
#print(test_data.marks[0])

# X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
# y = np.array([1, 1, 2, 2, 3, 3])

