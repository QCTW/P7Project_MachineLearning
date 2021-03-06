from tf_idf import TfIdf
from data_io import Data
from utility import merge_csr_matrix_by_col, expends
from features import count_all_capital_words, count_rarity_of_words
from classification import benchmark, Classify, find_best_k_clf
from data_cleaner import clean

import sklearn
import nltk
import sys
import numpy as np
import matplotlib.pyplot as plt
print("FAN & HSIEH's ML Project. Uses Scikit-learn-"+sklearn.__version__+" NLTK-"+nltk.__version__)

console_mode = True if (len(sys.argv)>1 and sys.argv[1]=="-i") else False

#Text analysis algo
clinton_trump_tweets = "dataset/trump/clinton-trump-tweets_clean.csv"
tf_idf = TfIdf(clinton_trump_tweets, 6)
Y = tf_idf.get_Y()
Y_labels = tf_idf.get_unique_Y()
X_top_1000_vocab, F_top_1000_vocab = tf_idf.get_X_by_vocabulary()
X_top_1000_bigram, F_top_1000_bigram = tf_idf.get_X_by_n_gram(2)
#X_top_1000_trigram, F_top_1000_trigram = tf_idf.get_X_by_n_gram(3)
X_all_capital_count = count_all_capital_words(tf_idf.data.text)
X_rarity_of_words = count_rarity_of_words(tf_idf.data.text)
X_main = merge_csr_matrix_by_col(X_top_1000_vocab, X_top_1000_bigram)
#X_main = merge_csr_matrix_by_col(X_main, X_top_1000_trigram)
X_main = merge_csr_matrix_by_col(X_main, X_all_capital_count)
X_main = merge_csr_matrix_by_col(X_main, X_rarity_of_words)
print("Total (Records, Features): "+str(X_main.shape))

tf_idf.data.shuffle_and_split(X_main, Y)

cfs = Classify()
x_train, y_train = tf_idf.data.get_train_data()
x_test, y_test = tf_idf.data.get_test_data()
results = []
for (clf, cl_name) in cfs.classifiers:
	results.append(benchmark(clf, x_train, y_train, x_test, y_test, Y_labels))

all_feature_names = tf_idf.vocab_features+tf_idf.n_gram_features+["Capital Words","Difficult Vocabs","Med-difficult Vocabs"]
all_features = []
c = 0
for n in cfs.classifiers[6][0].feature_importances_:
	all_features.append((c, n))
	c+=1

all_features.sort(key=lambda tup: float(tup[1]), reverse=True)
print('=' * 80)
print("Top 100 important features by "+cfs.classifiers[6][1]+": ")
c = 0
out = ""
for (i, n) in all_features[:100]:
	c+=1
	out += "["+all_feature_names[i] + "] "
	#out += "\""+all_feature_names[i] + "\":"+"{0:.4f}".format(n)+" "
	if(c%5 == 0):
		print(out)
		out = ""
print('=' * 80)
# find_best_k_clf(x_train, y_train, x_test, y_test, "knn", 5, 10, 60, n_fold = 5)

if( not console_mode):
	# make some plots
	indices = np.arange(len(results))
	results = [[x[i] for x in results] for i in range(4)]
	
	clf_names, score, training_time, test_time = results
	training_time = np.array(training_time) / np.max(training_time)
	test_time = np.array(test_time) / np.max(test_time)
	
	plt.figure(figsize=(12, 8))
	plt.title("Score")
	plt.barh(indices, score, .2, label="Score", color='darkorange')
	plt.barh(indices + .2, training_time, .2, label="Training time", color='navy')
	plt.barh(indices + .4, test_time, .2, label="Test time", color='c')
	plt.yticks(())
	plt.legend(loc='best')
	plt.subplots_adjust(left=.25)
	plt.subplots_adjust(top=.95)
	plt.subplots_adjust(bottom=.05)
	
	for i, c in zip(indices, clf_names):
		plt.text(-.3, i, c)
	
	plt.show()
########## Console Interactive Mode ##########
def find_index_from_labels(label, labels):
	for i in range(len(labels)):
		if(label == labels[i]):
			return i
	print("Unable to find class label: "+label)
	return -1

def single_predicte_forest(input_txt, tf_idf, cfs, X_top_1000_vocab, F_top_1000_vocab, X_top_1000_bigram, F_top_1000_bigram):
	X_top_vocab, F_top_vocab = tf_idf.get_X_by_vocabulary(input_txt)
	X_top_1000_vocab = expends(X_top_vocab, F_top_vocab, X_top_1000_vocab, F_top_1000_vocab)
	X_top_bigram, F_top_bigram = tf_idf.get_X_by_n_gram(2, input_txt)
	X_top_1000_bigram = expends(X_top_bigram, F_top_bigram, X_top_1000_bigram, F_top_1000_bigram)
	X_all_capital_count = count_all_capital_words(input_txt)
	X_rarity_of_words = count_rarity_of_words(input_txt)
	X_single = merge_csr_matrix_by_col(X_top_1000_vocab, X_top_1000_bigram)
	X_single = merge_csr_matrix_by_col(X_single, X_all_capital_count)
	X_single = merge_csr_matrix_by_col(X_single, X_rarity_of_words)
	clf = cfs.get_ridge_clf()
	#clf.fit(x_train, y_train)
	res = clf.predict(X_single)
	#idx = find_index_from_labels(res, Y_labels)
	#proba = clf.predict_proba(X_single)
	print("[!] Your text looks like: "+str(res[0])+" by "+cfs.classifiers[2][1]+".")

if(console_mode):
	print('=' * 80)
	print("[!] Now it's your turn to input some text and try our prediction!")
	line = input("[?] Please input some text (more than 20 words):\n")
	while (line != 'exit'):
		if len(line) < 20:
			line = input("[!] Your text is too short (<20), please try again:\n")
		else:
			clean_line = clean(line)
			single_predicte_forest([clean_line], tf_idf, cfs, X_top_1000_vocab, F_top_1000_vocab, X_top_1000_bigram, F_top_1000_bigram)
			line = input("[?] Please input some text (more than 20 words):\n")
	
	print("[!] Bye!")