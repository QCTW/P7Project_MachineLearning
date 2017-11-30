# This class is used for loading intermediate output file or raw file as an object
class Data:
	def __init__(self, key_path):
		f = open(key_path, 'r')
                self.text = []
		self.marks = []
                for line in f:
                        one_line = line.strip()
                        if(len(one_line)!=0):
				index_of_tab = one_line.find('\t')
				if(index_of_tab>0):
					first_col = one_line[:index_of_tab]
					second_col = one_line[index_of_tab+1:].strip()
					self.text.append(second_col)
					self.marks.append(first_col)
                                	print("["+first_col+"] "+second_col)
				else:
					self.text.append(one_line)
		f.close()


#test_data = Data("../spider/realDonaldTrump.csv")
#print(test_data.text)
