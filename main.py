from tf_idf import TfIdf
from data_io import Data
from utility import merge_csr_matrix_by_col
from features import count_all_capital_words
from classification import benchmark, Classify

import sklearn
print("Uses scikit-learn version: "+sklearn.__version__)

#Text analysis algo
clinton_trump_tweets = "dataset/trump/clinton-trump-tweets_clean.csv"
tf_idf = TfIdf(clinton_trump_tweets)
Y = tf_idf.get_Y()
X_top_1000_vocab = tf_idf.get_X_by_vocabulary()
X_top_1000_bigram = tf_idf.get_X_by_n_gram(2)
X_all_capital_count = count_all_capital_words(tf_idf.data.text)
X_main = merge_csr_matrix_by_col(X_top_1000_vocab, X_top_1000_bigram)
X_main = merge_csr_matrix_by_col(X_main, X_all_capital_count)
print("Total X-Features input: "+str(X_main.shape))

tf_idf.data.shuffle_and_split(X_main, Y)

cfs = Classify()
x_train, y_train = tf_idf.data.get_train_data()
print(str(y_train))
x_test, y_test = tf_idf.data.get_test_data()
print(str(y_test))
for (clf, cl_name) in cfs.classifiers:
	if(cl_name=="K Neighbors"):
		for n in range(1, 10):
			clf = cfs.get_k_neighbors_clf(n);
			benchmark(clf, x_train, y_train, x_test, y_test)
	else:
		benchmark(clf, x_train, y_train, x_test, y_test)