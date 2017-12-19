import re
import string
import nltk

from nltk.stem.porter import PorterStemmer
from utility import create_csr_matrix
from vocabulary_rarity import VocabularyRarity

def count_imperative_sentence(text_array):
	nltk.download('averaged_perceptron_tagger')
	for t in text_array:
		t.replace('\n', '\t')
		phrases = re.split(r"[\.\?\!]\s+", t)#re.compile("[A-Za-z0-9, ]+[.?!]+ ").split(t)
		for f in phrases:
			print(f)
			nltk.pos_tag(f)

def count_punctuation(text_array):
	count_list = []
	total = 0
	for t in text_array:
		#To count the number of terms in FULL capital in each text t
		t.replace('\n', '\t')
		#res = re.findall(r"[" + string.punctuation + "]", t)
		res = re.findall(r"[,]", t)
		t = re.sub(r"[" + string.punctuation + "]", "", t)
		tokens = t.split(' ')
		for word in tokens:
			if (len(word.strip())>0) :
				total+=1
		count_list.append([len(res)/total]) #Appends a one element array in each element of count_list
	return create_csr_matrix(count_list)

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
#test=["This is a phrase. And 2nd one... 3rd one. Make U.S great again! More ,and more? no,no,no..."]
#count_imperative_sentence(test)
#test=["The astronomer, perhaps, at this point, took refuge in the suggestion of non luminosity; and here analogy was suddenly let fall."]
#test=["Franchising America adorn", "MAKE U.S inane again", "MAKE Shanghai Sublime AGAIN", "DONALD.J.TRUMP"]
#csrm = count_punctuation(test)
#print(csrm.todense())
#csrm = count_rarity_of_words(test)
#print(csrm.todense())
