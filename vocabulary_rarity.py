
class VocabularyRarity:
	def __init__(self):
		# Data source : https://sites.google.com/site/sesamewords/home/mid-frequency-sat-1350-words
		self.low_freq_set = read_from_file("dataset/low-frequency-sat.txt")
		self.mid_freq_set = read_from_file("dataset/mid-frequency-sat.txt")
	
	def is_low_freq(self, vocab):
		return True if vocab in self.low_freq_set else False

	def is_mid_freq(self, vocab):
		return True if vocab in self.mid_freq_set else False

def read_from_file(fpath):
	vocabs = []
	f = open(fpath, 'r')
	for line in f:
		one_line = line.strip()
		if(len(one_line)!=0):
			index_of_dot = one_line.find('.')
			if(index_of_dot>0):
				first_col = one_line[:index_of_dot].strip()
				vocabs.append(first_col)
				print(first_col)
	
	f.close()
	return set(vocabs)

####################
# Unit test section
####################
#vr = VocabularyRarity()
#print(str(vr.is_low_freq("allocate")))
#print(str(vr.is_mid_freq("allocate")))