import tf_idf
import data_io
import scipy.sparse as sp

#Quick utilities
def merge_csr_matrix(csr_m1, scr_m2):
	return sp.vstack((scr_m1, src_m2))


#Text analysis algo
clinton-trump-tweets = "dataset/trump/clinton-trump-tweets_clean.csv"
tf_idf = TfIdf(clinton-trump-tweets)



