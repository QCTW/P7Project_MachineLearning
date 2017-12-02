import csv
import re


# to read the data_set contain trump and clinton
def read_mix_set(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            if line['handle'] == "realDonaldTrump":
                data.append(line['text'])
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
# data_set = read_mix_set('clinton-trump-tweets.csv')
# print(len(data_set))
# data_set = read_pure_set('trump-tweets.csv')
# print(len(data_set))
data_set = read_pure_set_bis('trump-tweets-bis.csv')
print(len(data_set))
print_some_line(data_set, 0, 50)


# remove the content which is around with " ... "
def remove_reference(data):
    return_data = []
    refer_content = []
    count = 0
    for line in data:
        list_refers = re.findall(r'\".*\"', line)
        if list_refers:
            refer_content.append([count, re.findall(r'\".*\"', line)])
        return_data.append(re.sub(r'\".*\"', '__QUOTE__', line))
        count += 1
    return return_data, refer_content


def write_clean_data(data):
    with open("../clean_data.txt",'w+') as output:
        for line in data:
            output.write(line+'\n')


def write_refers(data):
    with open("../references.txt",'w+') as output:
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






