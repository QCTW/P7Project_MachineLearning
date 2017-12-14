import re
import string

from nltk.stem.porter import PorterStemmer
from utility import create_csr_matrix
from vocabulary_rarity import VocabularyRarity

def count_all_capital_words(text_array):
	print("Counting all capital words...")
	count_list = []
	total = 0
	for t in text_array:
		#To count the number of terms in FULL capital in each text t
		count = 0
		t.replace('\n', '\t')
		t = re.sub(r"[" + string.punctuation + "]", "", t)
		tokens = t.split(' ')
		for word in tokens:
			if (len(t.strip())>0) :
				total+=1
				if word.isupper():
					count += 1
		count_list.append([count/total]) #Appends a one element array in each element of count_list
	return create_csr_matrix(count_list)

def count_rarity_of_words(text_array):
	print("Counting rarity of words...")
	count_list = []
	vr = VocabularyRarity()
	for t in text_array:
		t.replace('\n', '\t')
		t = re.sub(r"[" + string.punctuation + "]", "", t)
		tokens = t.split(' ')
		stemmer = PorterStemmer()
		tokens_to_roots = [stemmer.stem(t) for t in tokens]
		low_count = 0
		mid_count = 0
		total = 0
		for t in tokens_to_roots:
			if (len(t.strip())>0) :
				total+=1
				if (vr.is_low_freq(vocab=t)):
					low_count+=2
				elif (vr.is_mid_freq(vocab=t)):
					mid_count+=1
		count_list.append([low_count/total, mid_count/total])

	return create_csr_matrix(count_list)

####################
# Unit test section
####################
#test=["Franchising America adorn", "MAKE U.S inane again", "MAKE Shanghai Sublime AGAIN", "DONALD.J.TRUMP"]
#csrm = count_all_capital_words(test)
#print(csrm.todense())
#csrm = count_rarity_of_words(test)
#print(csrm.todense())
