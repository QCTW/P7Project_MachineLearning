import os
import csv
import re


# to read the data_set contain trump and clinton
def read_mix_set(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            if line['handle'] == "realDonaldTrump":
                data.append(('DonaldTrump', line['text']))
            else:
                data.append((line['handle'], line['text']))
    return data


# to read the data_set whose size is 1.6M
def read_pure_set(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append(('DonaldTrump', line['Tweet_Text']))
    return data


# to read the data_set whose size is 4.8M
def read_pure_set_bis(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append(('DonaldTrump', line['Text']))
    return data


# to read the other's tweets
def read_other_tweets(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append((line['author'], line['text']))
    return data

def clean(line_text):
    clean_text = line_text
    list_refers = re.findall(r'\".*\"', line_text)
    if list_refers:
        clean_text = re.findall(r'\".*\"', line_text)
    
    clean_text = re.sub(r'\".*\"', ' __QUOTE__ ', clean_text)
    clean_text = re.sub(r'https://\S*', ' __URL__ ', clean_text)
    clean_text = re.sub(r'\n', ' ', clean_text)
    return clean_text
    
# remove the content which is around with " ... " with ' __QUOTE__ '
def remove_reference(data):
    return_data = []
    refer_content = []
    count = 0
    for line in data:
        line_text = line[1]
        list_refers = re.findall(r'\".*\"', line_text)
        # list_urls = re.findall(r'https://\S*', line_text)
        if list_refers:
            refer_content.append((count, re.findall(r'\".*\"', line[1])))
        # if list_urls:
        #    print(line_text)
        #    for url in list_urls:
        #        print(url)

        line_text = re.sub(r'\".*\"', ' __QUOTE__ ', line_text)
        line_text = re.sub(r'https://\S*', ' __URL__ ', line_text)
        line_text = re.sub(r'\n', ' ', line_text)
        return_data.append([line[0], line_text])
        count += 1
    return return_data, refer_content


def write_clean_data(data, write_path):
    with open(write_path, 'w+') as output:
        for line in data:
            output.write(line[0]+'\t'+line[1]+'\n')


def append_new_clean_data(data, write_path):
    with open(write_path, 'a+') as output:
        for line in data:
            output.write(line[0] + '\t' + line[1] + '\n')


def write_refers(data, write_path):
    with open(write_path, 'w+') as output:
        for line in data:
            tmp_str = str(line[0])
            for refer in line[1]:
                tmp_str = tmp_str + '\t'+refer
            tmp_str += '\n'
            output.write(tmp_str)


def append_refers(data, write_path):
    with open(write_path, 'a+') as output:
        for line in data:
            tmp_str = str(line[0])
            for refer in line[1]:
                tmp_str = tmp_str + '\t'+refer
            tmp_str += '\n'
            output.write(tmp_str)

####################
# Unit test section
####################
# raw_file = "dataset/trump/clinton-trump-tweets.csv"
# raw_dir = os.path.dirname(raw_file)
# data_set = read_mix_set(raw_file)
# print(len(data_set))
# 
# clean_data_path = raw_dir+"/clinton-trump-tweets_clean.csv"
# refers_path = raw_dir+"/references.txt"
# (data_set_pure_text, refers) = remove_reference(data_set)
# print(len(data_set_pure_text))
# write_clean_data(data_set_pure_text, clean_data_path)
# write_refers(refers, refers_path)
# 
# data_set_obama = read_other_tweets("dataset/BarackObama.csv")
# print(len(data_set_obama))
# (data_set_clean_obama, refers_obama) = remove_reference(data_set_obama)
# print(len(data_set_clean_obama))
# append_new_clean_data(data_set_clean_obama, clean_data_path)
# append_refers(refers_obama, refers_path)
# 
# data_set_adam = read_other_tweets("dataset/AdamSavage.csv")
# print(len(data_set_adam))
# (data_set_clean_adam, refers_adam) = remove_reference(data_set_adam)
# print(len(data_set_clean_adam))
# append_new_clean_data(data_set_clean_adam, clean_data_path)
# append_refers(refers_adam, refers_path)
# 
# data_set_kim = read_other_tweets("dataset/KimKardashian.csv")
# print(len(data_set_kim))
# (data_set_clean_kim, refers_kim) = remove_reference(data_set_kim)
# print(len(data_set_clean_kim))
# append_new_clean_data(data_set_clean_kim, clean_data_path)
# append_refers(refers_kim, refers_path)
# 
# data_set_richard = read_other_tweets("dataset/RichardDawkins.csv")
# print(len(data_set_richard))
# (data_set_clean_richard, refers_richard) = remove_reference(data_set_richard)
# print(len(data_set_clean_richard))
# append_new_clean_data(data_set_clean_richard, clean_data_path)
# append_refers(refers_richard, refers_path)