import scipy.sparse as sp
import numpy as np
import re
import string

def create_csr_matrix(double_array):
	shape = (len(double_array), len(double_array[0]))
	row_index = []
	col_index = []
	flat_array = []
	for i in range(len(double_array)):
		arr = double_array[i]
		print(arr)
		for j in range(len(arr)):
			print(arr[j])
			if(arr[j]!=0):
				flat_array.append(arr[j])
				row_index.append(i)
				col_index.append(j)
				print("Append("+str(i)+","+str(j)+")")

	rows = np.array(row_index)
	cols = np.array(col_index)
	np_array = np.array(flat_array)
	return sp.csr_matrix( (np_array, (rows, cols)),  shape)


def count_all_capital_words(text_array):
	# Return a csr_matrix
	count_list = []
	for t in text_array:
		#TODO: To count the number of terms in FULL capital in each text t
		count = 0
		t.replace('\n', '\t')
		t = re.sub(r"[" + string.punctuation + "]", "", t)
		tokens = t.split(' ')
		for word in tokens:
			if word.isupper():
				count += 1
		count_list.append([count]) #Appends a one element array in each element of count_list
	return create_csr_matrix(count_list)


test=["Aaa MAKE", "BBB time", "CCC Shanghai", "DONALD TRUMP"]
print(count_all_capital_words(test))

