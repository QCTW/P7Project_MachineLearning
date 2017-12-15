from tf_idf import TfIdf
from data_csv import CsvData
from utility import merge_csr_matrix_by_col, expends
from features import count_all_capital_words, count_rarity_of_words, count_punctuation
from classification import benchmark, Classify, find_best_k_clf
from data_cleaner import clean
from time import time

import sklearn
import nltk
import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt

def algo(input_arr, top_1000_vocab, top_1000_bigram):
    X_all_capital_count = count_all_capital_words(input_arr)
    X_rarity_of_words = count_rarity_of_words(input_arr)
    X_punctuation_sparse = count_punctuation(input_arr)
    X_main = merge_csr_matrix_by_col(top_1000_vocab, top_1000_bigram)
    X_main = merge_csr_matrix_by_col(X_main, X_all_capital_count)
    X_main = merge_csr_matrix_by_col(X_main, X_rarity_of_words)
    X_main = merge_csr_matrix_by_col(X_main, X_punctuation_sparse)
    return X_main
    
stories = CsvData("dataset/ghost_story/train.csv")
tf_idf = TfIdf(num_of_class=3)
tf_idf.set_data(stories)
Y = tf_idf.get_Y()
Y_labels = tf_idf.get_unique_Y()
X_top_1000_vocab, F_top_1000_vocab = tf_idf.get_X_by_vocabulary()
X_top_1000_bigram, F_top_1000_bigram = tf_idf.get_X_by_n_gram(2)
X_main = algo(tf_idf.data.text, X_top_1000_vocab, X_top_1000_bigram)
print("Total (Records, Features): "+str(X_main.shape))

tf_idf.data.shuffle_and_split(X_main, Y)

cfs = Classify()
x_train, y_train = tf_idf.data.get_train_data()
x_test, y_test = tf_idf.data.get_test_data()
results = []
for (clf, cl_name) in cfs.classifiers:
    results.append(benchmark(clf, x_train, y_train, x_test, y_test, Y_labels))

clf_naive_bayes = cfs.get_multinomial_naive_bayes()
t0 = time()
clf_naive_bayes.fit(X_main, Y)
train_time = time() - t0
print("Training time: %0.3fs" % train_time)

to_pred = CsvData("dataset/ghost_story/test.csv")

X_top_1000_vocab, F_top_1000_vocab = tf_idf.get_X_by_vocabulary(to_pred.text)
X_top_1000_bigram, F_top_1000_bigram = tf_idf.get_X_by_n_gram(2, to_pred.text)
X_main = algo(to_pred.text, X_top_1000_vocab, X_top_1000_bigram)
t0 = time()
pred_proba = clf_naive_bayes.predict_proba(X_main)
test_time = time() - t0
print("Predict time:  %0.3fs" % test_time)
str_header = "\"id\",\"EAP\",\"HPL\",\"MWS\""
print(clf_naive_bayes)
with open("./sai_prediction.csv", 'w+') as output:
    output.write(str_header+'\n')
    for i in range(len(pred_proba)):
        msg = "\""+to_pred.ids[i]+"\","+str(pred_proba[i, 0])+","+str(pred_proba[i, 1])+","+str(pred_proba[i, 2])
        output.write(msg+'\n')
