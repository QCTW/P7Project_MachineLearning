import re
import string

from utility import create_csr_matrix

def count_all_capital_words(text_array):
	count_list = []
	for t in text_array:
		#To count the number of terms in FULL capital in each text t
		count = 0
		t.replace('\n', '\t')
		t = re.sub(r"[" + string.punctuation + "]", "", t)
		tokens = t.split(' ')
		for word in tokens:
			if word.isupper():
				count += 1
		count_list.append([count]) #Appends a one element array in each element of count_list
	return create_csr_matrix(count_list)


test=["Make America great again", "MAKE U.S great again", "MAKE Shanghai Great AGAIN", "DONALD.J.TRUMP"]
csrm = count_all_capital_words(test)
print(csrm.todense())

