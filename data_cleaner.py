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
                data.append((1,line['text']))
            else:
                data.append((0, line['text']))
    return data


# to read the data_set whose size is 1.6M
def read_pure_set(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append(line['Tweet_Text'])
    return data


# to read the data_set whose size is 4.8M
def read_pure_set_bis(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append(line['Text'])
    return data


def print_some_line(data, start, end):
    for line in data[start:end]:
        print(line)
    print()

raw_file = "dataset/trump/clinton-trump-tweets.csv"
raw_dir = os.path.dirname(raw_file)
data_set = read_mix_set(raw_file)
# data_set = read_pure_set(raw_file)
# data_set = read_pure_set_bis(raw_file)
print(len(data_set))
print_some_line(data_set, 0, 50)


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
        return_data.append([line[0], line_text])
        count += 1
    return return_data, refer_content


def write_clean_data(data):
    with open(raw_dir+"/clean_data.txt", 'w+') as output:
        for line in data:
            output.write(str(line[0])+'\t'+line[1]+'\n')


def write_refers(data):
    with open(raw_dir+"/references.txt", 'w+') as output:
        for line in data:
            tmp_str = str(line[0])
            for refer in line[1]:
                tmp_str = tmp_str + '\t'+refer
            tmp_str += '\n'
            output.write(tmp_str)


(data_set_pure_text, refers) = remove_reference(data_set)
print(len(data_set_pure_text))
print_some_line(data_set_pure_text, 0, 50)
print_some_line(refers, 0, 10)
write_clean_data(data_set_pure_text)
write_refers(refers)
